#!/usr/bin/env python

import os
import ember
import argparse
import lightgbm as lgb

from sklearn.metrics import accuracy_score

# Function to get predictions
def predict(model,X,y,rows):
    # Run predictions
    lgbm_dataset = lgb.Dataset(X[rows], y[rows])
    predicted = model.predict(lgbm_dataset.data)

    # Apply threshold
    predicted[(predicted >= 0.871)] = 1
    predicted[(predicted < 0.871)] = 0

    # Get accuracy
    return accuracy_score(y[rows],predicted)

def main():
    prog = "test_ember"
    descr = "Test an ember model from a directory with raw feature files"
    parser = argparse.ArgumentParser(prog=prog, description=descr)
    parser.add_argument("-v", "--featureversion", type=int, default=2, help="EMBER feature version", required=False)
    parser.add_argument("-m", "--modelpath", type=str, default=None, required=True, help="Ember model")
    parser.add_argument("--datadir", type=str, help="Directory with raw features",required=True)
    args = parser.parse_args()

    if not os.path.exists(args.datadir) or not os.path.isdir(args.datadir):
        parser.error("{} is not a directory with raw feature files".format(args.datadir))

    X_train_path = os.path.join(args.datadir, "X_train.dat")
    y_train_path = os.path.join(args.datadir, "y_train.dat")
    if not (os.path.exists(X_train_path) and os.path.exists(y_train_path)):
        print("Creating vectorized features")
        ember.create_vectorized_features(args.datadir)

    if not os.path.exists(args.modelpath):
        parser.error("ember model {} does not exist".format(args.modelpath))

    print("Testing LightGBM model")

    # Load model
    lgbm_model = lgb.Booster(model_file=args.modelpath)

    # Read data
    X_train, y_train = ember.read_vectorized_features(args.datadir, subset="train", feature_version=args.featureversion)
    X_test, y_test = ember.read_vectorized_features(args.datadir, subset="test", feature_version=args.featureversion)

    # Filter unlabeled data
    train_rows = (y_train != -1)
    test_rows = (y_test != -1)

    # Run predictions
    accuracy = predict(lgbm_model,X_train,y_train,train_rows)
    print("Training Accuracy: {0}".format(accuracy))

    accuracy = predict(lgbm_model,X_test,y_test,test_rows)
    print("Testing Accuracy: {0}".format(accuracy))

if __name__ == "__main__":
    main()
