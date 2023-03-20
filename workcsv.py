import pandas
from pathlib import Path
from csv import writer

def write_data(id, role, request, response):
    if Path('data/'+role+'_'+str(id)+'.csv').is_file():
        with open('data/'+role+'_'+str(id)+'.csv', 'a') as file:
            writer_object = writer(file)
            writer_object.writerow([request if role == 'user' else response])
            file.close()
    else:
        filepath = Path('data/'+role+'_'+str(id)+'.csv')  
        filepath.parent.mkdir(parents=True, exist_ok=True)
        par = 'request' if role == 'user' else 'response'
        df = pandas.DataFrame({par: []})
        df.to_csv(filepath)
        print('created new csv!')
        write_data(id, role, request, response)
        
def read_data(id):
    pass