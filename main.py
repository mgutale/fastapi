from fastapi import FastAPI, Path, Query
from typing import Optional
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

df = pd.read_csv("data/test.csv")

@app.get("/")
def home():
    return {"Test Poscodes": df["PostCode"].values.tolist()}

# query api
inventory = {
    1: {
        "name" : "Milk",
        "price": 3.99,
        "brand": "Regular"
    }    
}
#path parameters
@app.get("/get-item/{item_id}")
def get_item(item_id:int):
    return inventory[item_id]

# mutliple path parameters 
@app.get("/get-item/{item_id}/{name}")
def get_item(item_id:int, name:str):
    return inventory[item_id][name]

# add more details to the parameter that the user would like tp pass as well as adding constraints 
@app.get("/get-item/{item_id}")
#None refers to default value if none is passed and gt refers to greater than zero
def get_item(item_id:int = Path(None, description="The ID that you would like to pass must be greater than 0", gt= 0)):
    return inventory[item_id]

#query parameter #localhost:8000/get-by-name/name=Milk
#@app.get("/get-by-name")
#def get_item(name:str):
 #   for item_id in inventory:
  #      if inventory[item_id]['name'] = name:
   #         return inventory[item_id]
    #return {"Data": "Data Not found"}

#query parameter making default argument optional #localhost:8000/get-by-name/name=Milk
#@app.get("/get-by-name")
#def get_item(*, name: Optional[str]=None, test: int):
    #for item_id in inventory:
       # if inventory[item_id]['name'] = name:
       #     return inventory[item_id]
   # return {"Data": "Data Not found"}

#create an item
#define a base model of type of data to accept into the post
class Item(BaseModel):
    name:str
    price:float
    brand: Optional[str] =None
    
@app.post("/create-item/{item_id}")
def create_item(item_id:int, item: Item):
    if item_id in inventory:
        return {"Error": "Item Id already exists"}
    inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
    return inventory[item_id]
    
#update

#define a base model of type of data to accept into the post
class Update_Item(BaseModel):
    name:str = None
    price:float = None
    brand: Optional[str] = None
    
@app.put("/update-item/{item_id}")
def update_item(item_id:int, item:Update_Item):
    if item_id not in inventory:
        return {"Error": "Item Id does not exists"}
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id] 

# delete item
@app.delete("/delete-item")
def delete_item(item_id: int= Query(..., description = "the ID of the old item to delete")):
    if item_id not in inventory:
        return {"Error": "ID does not exist"}
    
    del inventory[item_id]
        
    
