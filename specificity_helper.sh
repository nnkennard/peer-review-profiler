# These steps are part of the Domain Agnostic Specificity Prediction pipeline
. /work/pi_mccallum_umass_edu/nnayak_umass_edu/miniconda3/etc/profile.d/conda.sh && conda activate profiler_specificity_env
cd Domain-Agnostic-Sentence-Specificity-Prediction/
python test.py --gpu_id 0 --test_data twitter 
