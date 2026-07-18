/* FW-2 — esp-tflite-micro / IDF v6.0.2 compat spike (fw_execution_layer.md E-2).
 *
 * Exercises exactly what the D-9 wake stack needs from the component:
 *  1) the feature pipeline — the SIGNAL-LIB audio preprocessor (Window → FftAutoScale →
 *     Rfft → Energy → FilterBank → sqrt/spectral-subtraction/PCAN/log), registered as
 *     TFLM ops so the whole signal/ + kissfft path must compile AND link;
 *  2) the TFLM core — interpreter + op resolver + an int8 classifier invoke at
 *     micro_speech scale (DepthwiseConv2D / FullyConnected / Softmax / Reshape).
 *
 * NB the task text named the "TFLite-Micro micro-features frontend"
 * (tensorflow/lite/experimental/microfrontend): that lib is NOT in the 1.3.7
 * distribution — upstream removed it; the component's CMake GLOB of it is vestigial.
 * The signal lib is its successor and is what ships; the FW-2 verdict records this.
 *
 * Model data + pipeline constants adapted from the component's own
 * examples/micro_speech (Apache-2.0, The TensorFlow Authors — see model.h /
 * audio_preprocessor_int8_model_data.h headers).
 */

#include <algorithm>
#include <cmath>
#include <cstdio>

#include "audio_preprocessor_int8_model_data.h"
#include "model.h"
#include "tensorflow/lite/kernels/internal/tensor_ctypes.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"

namespace {

// micro_speech training-time constants (micro_model_settings.h upstream).
constexpr int kAudioSampleFrequency = 16000;
constexpr int kFeatureSize = 40;
constexpr int kFeatureCount = 49;
constexpr int kFeatureElementCount = kFeatureSize * kFeatureCount;
constexpr int kFeatureStrideMs = 20;
constexpr int kFeatureDurationMs = 30;
constexpr int kSamplesPerWindow = kFeatureDurationMs * kAudioSampleFrequency / 1000;
constexpr int kSamplesPerStride = kFeatureStrideMs * kAudioSampleFrequency / 1000;
constexpr int kAudioLen = kSamplesPerWindow + (kFeatureCount - 1) * kSamplesPerStride;

alignas(16) uint8_t g_feature_arena[16 * 1024];
alignas(16) uint8_t g_model_arena[30 * 1024];
int16_t g_audio[kAudioLen];
int8_t g_features[kFeatureElementCount];

using FeatureOpResolver = tflite::MicroMutableOpResolver<18>;
using ModelOpResolver = tflite::MicroMutableOpResolver<4>;

bool RegisterFeatureOps(FeatureOpResolver& r) {
  return r.AddReshape() == kTfLiteOk && r.AddCast() == kTfLiteOk &&
         r.AddStridedSlice() == kTfLiteOk && r.AddConcatenation() == kTfLiteOk &&
         r.AddMul() == kTfLiteOk && r.AddAdd() == kTfLiteOk && r.AddDiv() == kTfLiteOk &&
         r.AddMinimum() == kTfLiteOk && r.AddMaximum() == kTfLiteOk &&
         r.AddWindow() == kTfLiteOk && r.AddFftAutoScale() == kTfLiteOk &&
         r.AddRfft() == kTfLiteOk && r.AddEnergy() == kTfLiteOk &&
         r.AddFilterBank() == kTfLiteOk && r.AddFilterBankSquareRoot() == kTfLiteOk &&
         r.AddFilterBankSpectralSubtraction() == kTfLiteOk && r.AddPCAN() == kTfLiteOk &&
         r.AddFilterBankLog() == kTfLiteOk;
}

}  // namespace

extern "C" void app_main(void) {
  // Synthetic 440 Hz test tone — the spike's verdict is compile+link (and, on a bench,
  // a sane invoke); it asserts nothing about recognition quality.
  for (int i = 0; i < kAudioLen; ++i) {
    g_audio[i] = static_cast<int16_t>(
        4000.0f * sinf(2.0f * static_cast<float>(M_PI) * 440.0f * i / kAudioSampleFrequency));
  }

  // 1) Feature pipeline: the signal-lib audio preprocessor model.
  const tflite::Model* fmodel = tflite::GetModel(g_audio_preprocessor_int8_tflite);
  if (fmodel->version() != TFLITE_SCHEMA_VERSION) {
    MicroPrintf("FW-2: preprocessor schema %lu != %d FAIL",
                static_cast<unsigned long>(fmodel->version()), TFLITE_SCHEMA_VERSION);
    return;
  }
  static FeatureOpResolver feature_ops;
  if (!RegisterFeatureOps(feature_ops)) {
    MicroPrintf("FW-2: signal-op registration FAIL");
    return;
  }
  static tflite::MicroInterpreter feature_interp(fmodel, feature_ops, g_feature_arena,
                                                 sizeof(g_feature_arena));
  if (feature_interp.AllocateTensors() != kTfLiteOk) {
    MicroPrintf("FW-2: preprocessor AllocateTensors FAIL");
    return;
  }
  const int16_t* audio = g_audio;
  for (int f = 0; f < kFeatureCount; ++f) {
    std::copy_n(audio, kSamplesPerWindow,
                tflite::GetTensorData<int16_t>(feature_interp.input(0)));
    if (feature_interp.Invoke() != kTfLiteOk) {
      MicroPrintf("FW-2: preprocessor Invoke FAIL at frame %d", f);
      return;
    }
    std::copy_n(tflite::GetTensorData<int8_t>(feature_interp.output(0)), kFeatureSize,
                &g_features[f * kFeatureSize]);
    audio += kSamplesPerStride;
  }
  MicroPrintf("FW-2: signal-lib features ok (%d frames x %d)", kFeatureCount, kFeatureSize);

  // 2) Classifier invoke: the micro_speech int8 model.
  const tflite::Model* model = tflite::GetModel(g_model);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    MicroPrintf("FW-2: model schema %lu != %d FAIL",
                static_cast<unsigned long>(model->version()), TFLITE_SCHEMA_VERSION);
    return;
  }
  static ModelOpResolver model_ops;
  if (model_ops.AddDepthwiseConv2D() != kTfLiteOk ||
      model_ops.AddFullyConnected() != kTfLiteOk || model_ops.AddSoftmax() != kTfLiteOk ||
      model_ops.AddReshape() != kTfLiteOk) {
    MicroPrintf("FW-2: model-op registration FAIL");
    return;
  }
  static tflite::MicroInterpreter interp(model, model_ops, g_model_arena,
                                         sizeof(g_model_arena));
  if (interp.AllocateTensors() != kTfLiteOk) {
    MicroPrintf("FW-2: model AllocateTensors FAIL");
    return;
  }
  TfLiteTensor* input = interp.input(0);
  if (input->type != kTfLiteInt8) {
    MicroPrintf("FW-2: unexpected input tensor type FAIL");
    return;
  }
  std::copy_n(g_features, kFeatureElementCount, tflite::GetTensorData<int8_t>(input));
  if (interp.Invoke() != kTfLiteOk) {
    MicroPrintf("FW-2: model Invoke FAIL");
    return;
  }
  const int8_t* scores = tflite::GetTensorData<int8_t>(interp.output(0));
  MicroPrintf("FW-2: PASS — invoke ok, scores [%d %d %d %d] (silence/unknown/yes/no)",
              scores[0], scores[1], scores[2], scores[3]);
}
