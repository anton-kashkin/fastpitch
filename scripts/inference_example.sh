#!/usr/bin/env bash

export CUDNN_V8_API_ENABLED=1

: ${DATASET_DIR:="alyona"}
: ${BATCH_SIZE:=2}
: ${FILELIST:="phrases/korzina_for_fastpitch.tsv"}
# : ${FILELIST:="phrases/benchmark_16_128.tsv"}
: ${AMP:=false}
: ${TORCHSCRIPT:=true}
: ${WARMUP:=20}
: ${REPEATS:=1}
: ${CPU:=false}

# Mel-spectrogram generator (optional)
: ${FASTPITCH="output/alyona_emotive_amp_test/FastPitch_checkpoint_1500.pt"}

# Vocoder; set only one
# : ${WAVEGLOW="pretrained_models/waveglow/nvidia_waveglow256pyt_fp16.pt"}
: ${WAVEGLOW=""}
: ${HIFIGAN=""}

# Synthesis
: ${SPEAKER:=0}
: ${DENOISING:=0.01}

if [ ! -n "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="./output/audio_from_amp_$(basename ${FILELIST} .tsv)"
    [ "$AMP" = true ]     && OUTPUT_DIR+="_fp16"
    [ "$AMP" = false ]    && OUTPUT_DIR+="_fp32"
    [ -n "$FASTPITCH" ]   && OUTPUT_DIR+="_fastpitch"
    [ ! -n "$FASTPITCH" ] && OUTPUT_DIR+="_gt-mel"
    [ -n "$WAVEGLOW" ]    && OUTPUT_DIR+="_waveglow"
    [ -n "$HIFIGAN" ]     && OUTPUT_DIR+="_hifigan"
    OUTPUT_DIR+="_denoise-"${DENOISING}
fi
OUTPUT_DIR="./output/test_korzinka"
: ${LOG_FILE:="$OUTPUT_DIR/custom_logs.json"}
mkdir -p "$OUTPUT_DIR"

echo -e "\nAMP=$AMP, batch_size=$BATCH_SIZE\n"

ARGS=""
ARGS+=" --save-mels"
# ARGS+=" --pitch-transform-flatten"
ARGS+=" --cuda"
# ARGS+=" --cudnn-benchmark"
ARGS+=" --dataset-path $DATASET_DIR"
ARGS+=" -i $FILELIST"
ARGS+=" -o $OUTPUT_DIR"
ARGS+=" --log-file $LOG_FILE"
ARGS+=" --batch-size $BATCH_SIZE"
ARGS+=" --denoising-strength $DENOISING"
ARGS+=" --warmup-steps $WARMUP"
ARGS+=" --repeats $REPEATS"
ARGS+=" --speaker $SPEAKER"
[ "$CPU" = false ]          && ARGS+=" --cuda"
# [ "$CPU" = false ]          && ARGS+=" --cudnn-benchmark"
[ "$AMP" = true ]         && ARGS+=" --amp"
[ "$TORCHSCRIPT" = true ] && ARGS+=" --torchscript"
[ -n "$HIFIGAN" ]         && ARGS+=" --hifigan $HIFIGAN"
[ -n "$WAVEGLOW" ]        && ARGS+=" --waveglow $WAVEGLOW"
[ -n "$FASTPITCH" ]       && ARGS+=" --fastpitch $FASTPITCH"

python inference.py $ARGS "$@"
