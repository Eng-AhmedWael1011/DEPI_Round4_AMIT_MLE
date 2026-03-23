from sklearn.model_selection import train_test_split

def split_data(data , predict_feature):
    """We will work with a training data of 80% with fixed training data AKA Random_state is set to any number"""
    x = data.drop(predict_feature , axis=1)
    y = data[predict_feature]

    return train_test_split(x , y , train_size=0.8 , random_state=42)