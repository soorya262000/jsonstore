from jsonstore import jsonstore
import time
js=jsonstore()
a={2:"asasdajlkjlkasdjlkjlkjasdasdasdasd","vv":[1,3,4]}
b={4:{"sdsdsdsd":2},"e":2}
print(js.configstore.get_stores())
print(js.configstore.get_open_stores())
datastore=js.open_store(r"C:\Users\soorya\Desktop\store.json")
print(js.configstore.get_open_stores())
print(datastore.get("a"))
print(datastore.add("a",a))
print(datastore.get("a"))
print(datastore.add("b",b,1))
print(datastore.get("b"))
#time.sleep(65)
#print(datastore.get("b"))
#print(datastore.delete("a"))
#print(datastore.get("a"))
js.exit()



