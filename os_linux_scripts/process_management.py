import subprocess
import sys
import os
import platform


print('+'*25 + ' 1. Список всех процессов ' + '+'*25)
args = ['ps', 'aux']
lst_all_processes = subprocess.Popen(args, stdout=subprocess.PIPE)
out = lst_all_processes.communicate()
print(out)


print('+'*25 + ' 2. Информацию о конкретном процессе ' + '+'*25)
args = ['ps', 'grep', '142']
info_about_process = subprocess.Popen(args, stdout=subprocess.PIPE)
out = info_about_process.communicate()
print(out)

print('+'*16 + ' 3. Список в файлов в директории (указать директорию)' + '+'*18)
print('+'*20 + ' 4. Текущую директорию и список в файлов в ней ' + '+'*20)
path = os.getcwd()
print(path)
path2 = path + '/tests'
os.chdir(path2)
print(os.getcwd())
lst_of_files_in_dir = subprocess.check_call(['ls', '-la'])

print('+'*30 + ' 5. Версию ядра' + '+'*30)
if (os.name == "posix"): print
os.system("uname -a")

print('+'*22 + ' 6. Версию операционной системы' + '+'*22)
print(platform.platform())


