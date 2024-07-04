from thirdai import neural_db as ndb

db = ndb.NeuralDB(retriever='finetunable_retriever')

train_file = "/home/sdp/MIT/mit_ocw.csv"
csv_doc = [ndb.CSV(train_file, id_column="Id", strong_columns=['Title','text'])]

db.insert(csv_doc)

db.save("model.ndb")


