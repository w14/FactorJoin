import argparse
import logging
import os
import time
import shutil
import numpy as np
import pandas as pd

from Evaluation.training import train_one_stats

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='stats', help='Which dataset to be used')

    # generate models/ensembles
    parser.add_argument('--generate_models', help='Trains BNs on dataset', action='store_true')
    parser.add_argument('--data_path', default='/home/ubuntu/End-to-End-CardEst-Benchmark/datasets/stats_simplified/{}.csv')
    parser.add_argument('--model_path', default='/home/ubuntu/data_CE/CE_scheme_models/')
    parser.add_argument('--n_bins', type=int, default=200, help="The bin size on the id attributes")
    parser.add_argument('--bucket_method', type=str, default="greedy", help="The bin size on the id attributes")
    parser.add_argument('--save_bucket_bins', help="Whether want to support data update", action='store_true')

    # evaluation
    parser.add_argument('--evaluate', help='Evaluates models to compute cardinality bound', action='store_true')
    parser.add_argument('--model_location', nargs='+', default='/home/ubuntu/data_CE/CE_scheme_models/model_stats_200.pkl')
    parser.add_argument('--query_file_location', default='/home/ubuntu/End-to-End-CardEst-Benchmark/workloads/stats_CEB/stats_CEB.sql')
    
    # get all sub_plan_query cardinalities
    parser.add_argument('--predict', help='estimate all sub_plan_query cardinalities', action='store_true')

    # log level
    parser.add_argument('--log_level', type=int, default=logging.DEBUG)

    args = parser.parse_args()

    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=args.log_level,
        # [%(threadName)-12.12s]
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler("logs/{}_{}.log".format(args.dataset, time.strftime("%Y%m%d-%H%M%S"))),
            logging.StreamHandler()
        ])
    logger = logging.getLogger(__name__)

    print(args.dataset)
    if args.dataset == 'stats':
        if args.generate_models:
            start_time = time.time()
            train_one_stats(args.dataset, args.data_path, args.model_path, args.n_bins, args.bucket_method, args.save_bucket_bins)
            end_time = time.time()
            print(f"Training completed: total training time is {end_time - start_time}")

