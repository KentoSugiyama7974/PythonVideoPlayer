import numpy as np
from numpy import fft
import math


class ImportData:
    def __init__(self,path):
        self.path = path
        self.game_num = path.split("/")[-2]
        self.team = {'1':[['C','D','F','G','J'],['A','B','E','H','I']],\
                    '2':[['A','D','E','G','I'],['B','C','F','H','J']],\
                    '3':[['B','D','F','G','J'],['A','C','E','H','I']]}
        self.open_file()

    def myfft(self,data):
        output_activity = np.array([])
        output_fft = []
        for norm in data:
            N = 128 
            avg = sum(norm)/len(norm)
            blank = N - len(norm)
            bef = blank//2
            af = blank - bef
            norm = [avg]*bef + norm + [avg]*af
            norm = [i-avg for i in norm]
            fft_data = fft.fft(norm)
            fft_data = abs(fft_data)
            fft_data = fft_data[:N//2]
            #activity_data
            output_activity = np.append(output_activity,sum(fft_data)/len(fft_data))
            #corrcoef用fft_data
            output_fft.append(fft_data)
        return output_activity,output_fft

    def mycorrcoef(self,list_data_a,list_data_b):
        output = np.empty(0)
        for index in range(len(list_data_a)):
            storage = np.corrcoef(list_data_a[index],list_data_b[index])
            output = np.append(output,storage[0,1])
        return output

    def open_file(self,sec=2):
        files = ['A','B','C','D','E','F','G','H','I','J']
        self.activity = {"A":[],"B":[],"C":[],"D":[],"E":[],"F":[],"G":[],"H":[],"I":[],"J":[]}
        get_fft = {"A":[],"B":[],"C":[],"D":[],"E":[],"F":[],"G":[],"H":[],"I":[],"J":[]}
        self.corrcoef = {}

        #A~Jのデータ取得
        for name in files:
            norm = []
            time = []
            norm_data = []
            self.time_data = []
            with open(self.path+name+".txt") as f:
                lines = f.readlines()
            #time, norm, 必要に応じて9軸センサデータ [x_acc, y_acc, z_acc, x_gyro, y_gyro, z_gyro, x_magnet, y_magnet, z_magnet]  
            time += [':'.join(str(line).split(",")[0].split("-")[1].split(".")[0:3]) for line in lines]
            nine_axis = [[float(i) for i in line.split(",")[1:]] for line in lines]
            norm += [np.sqrt(sum([i**2 for i in line[0:3]])) for line in nine_axis]
            #secごとに2次元データ作成
            for index in range(len(norm)//(60*sec)):
                norm_data.append(norm[index*60*sec:(index+1)*60*sec])
                self.time_data.append(time[index*60*sec])
            norm_data.append(norm[(index+1)*60*sec:])
            self.activity[name],get_fft[name] = self.myfft(norm_data)
        for index,x in enumerate(files[:-1]):
            for y in files[index+1:]:
                self.corrcoef[x+"_"+y] = self.mycorrcoef(get_fft[x],get_fft[y])
        self.team_datas_make()
    
    def team_datas_make(self):
        self.team_corrcoef = {"bibusu":0,"no_bibusu":0}
        self.team_activity = {"bibusu":0,"no_bibusu":0}
        for i,team in enumerate(["bibusu","no_bibusu"]):
            for index,x in enumerate(self.team[self.game_num[0]][i][:-1]):
                for y in self.team[self.game_num[0]][i][index+1:]:
                    self.team_corrcoef[team] += self.corrcoef[x+"_"+y]
            self.team_corrcoef[team] = self.team_corrcoef[team]/10        

            for x in self.team[self.game_num[0]][i]:
                self.team_activity[team] += self.activity[x]
            self.team_activity[team] = self.team_activity[team]/5

    def get_item(self):
        return self.activity,self.corrcoef,self.time_data

    def get_team_item(self):
        return self.team_activity,self.team_corrcoef,self.time_data

if __name__ == "__main__":
    a = ImportData("C:/Users/ymtlab/Documents/20210430/1_1/")
    a.team_datas_make()
    b,c,d = a.get_team_item()
    print(b)
