import pandas
from pathlib import Path
from csv import writer

data = {'role': [], 'content': []}

def write_data(id, role, r):
    if Path('data/data_'+str(id)+'.csv').is_file():
        with open('data/data_'+str(id)+'.csv', 'a') as file:
            writer_object = writer(file)
            writer_object.writerow([role, r])
            file.close()
    else:
        filepath = Path('data/data_'+str(id)+'.csv')  
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df = pandas.DataFrame(data)
        df.to_csv(filepath, index=False)
        print('created new csv!')
        write_data(id, role, r)
        
def read_data(id):
    file_path = Path('data/data_'+str(id)+'.csv')
    if file_path.is_file():
        df = pandas.read_csv(file_path)
        print(df)
        return list(df['content'])
    else:
        print('No such file exists!')
        return None
