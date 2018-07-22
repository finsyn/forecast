#! /bin/bash

# uploads all trained models and necessary metadata so it can be
# consumed by our CI pipeline

gsutil cp outputs/* gs://finsyn-ml-data/outputs/$(date +%F)/
