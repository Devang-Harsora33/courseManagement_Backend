import pymongo

url = "mongodb+srv://devangkh1206:admin123@coursesmanagement.v5dfb.mongodb.net/?retryWrites=true&w=majority&appName=coursesManagement"
# url = "mongodb://localhost:27017"
connection = pymongo.MongoClient(url)

db = connection['coursesManagement']
