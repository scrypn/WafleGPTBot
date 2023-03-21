import pandas
from pathlib import Path
from csv import writer

def write_data(id, role, request, response):
    if Path('data/'+role+'_'+str(id)+'.csv').is_file():
        with open('data/'+role+'_'+str(id)+'.csv', 'a') as file:
            writer_object = writer(file)
            if role == 'user': data = [request]
            else: data = [response]
            writer_object.writerow(data)
            file.close()
    else:
        filepath = Path('data/'+role+'_'+str(id)+'.csv')  
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if role == 'user': df = pandas.DataFrame({'request': []}) 
        else: df = pandas.DataFrame({'response': []})
        df.to_csv(filepath, index=False)
        print('created new csv!')
        write_data(id, role, request, response)
        
def read_data(id, role):
    file_path = Path('data/'+role+'_'+str(id)+'.csv')
    if file_path.is_file():
        df = pandas.read_csv(file_path)
        return list(df['request'])  
    else:
        print('No such file exists!')
        return None
