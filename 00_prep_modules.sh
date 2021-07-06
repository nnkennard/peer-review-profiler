#!/bin/bash

set -e

cur_dir=`pwd`

cd ReviewAdvisor/
bash download_tagger.sh
bash download_dataset.sh


