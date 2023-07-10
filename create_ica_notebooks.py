import os

for i in range(1, 21):
    for j in range(1, 3):
        if i <10:
            s = str(i)
            pid = '0'+s
        else:
            pid = str(i)
        sess = '0'+str(j)
        session = 'm_'+pid+'_'+sess
        nb_name = session+'.ipynb'
        os.system('cp m_00_02.ipynb '+nb_name)
