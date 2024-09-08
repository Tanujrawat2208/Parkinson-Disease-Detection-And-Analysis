import pickle 
import pandas as pd
import sys

class Prediction:
    def __init__(self, FileName):
        self.FileName = FileName

    def predict(self):

        df = pd.read_csv(self.FileName)
        model = pickle.load(open ('Model/model.pkl', 'rb')) 

        y_predict = model.predict(df)
        y_predict = (y_predict > 0.5).astype(int)

        zeros = (y_predict == 0).sum()
        ones = (y_predict == 1).sum()

        if zeros > ones:
            confidence = format((zeros / (ones + zeros)) * 100, ".2f")
            result = [0, confidence]
        else:
            confidence = format((ones / (ones + zeros)) * 100, ".2f")
            result = [1, confidence]
        return result

if __name__ == "__main__":
    args = sys.argv
    text_file_path = args[1]

    ob = Prediction(text_file_path)
    result = ob.predict()

    print(result)






    