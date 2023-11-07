# These steps are part of the ReviewAdvisor pipeline
. /work/pi_mccallum_umass_edu/nnayak_umass_edu/miniconda3/etc/profile.d/conda.sh && conda activate profiler_aspect_env
cd ReviewAdvisor/tagger/
bash prepare.sh sample.txt
python run_tagger.py config.json
bash post_process.sh

