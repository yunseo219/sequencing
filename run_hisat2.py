import os, sys, json, time, glob
import multiprocessing as mp
from multiprocessing import Pool, cpu_count

project = 'P_diamond_pilot'
date = '20201211'

start = time.time()
f = open('/data2/P_diamond_pilot/outputs/Tables/'+ project +'_table.json', "r")
samples = json.load(f)
f.close()

index = '/data2/P_diamond_pilot/fastq/data1'
cmds = []

for i in samples.keys():
	pwd = '/data2/P_diamond_pilot/fastq/' + i +'/'
	print('/'.join(['mkdir /data2', project, 'HISAT2/outputs', i]))
	os.system('/'.join(['mkdir /data2', project, 'HISAT2/outputs', i]))
	for s in samples[i]:
		print('/'.join(['mkdir /data2', project, 'HISAT2/outputs', i, s]))
		os.system('/'.join(['mkdir /data2', project, 'HISAT2/outputs', i, s]))
		R1 = glob.glob(pwd + s + '*R1*')[0]
		R2 = glob.glob(pwd + s + '*R2*')[0]
		o_file = '/'.join(['/data2', project, 'HISAT2/outputs', i, s, '.'.join([s, date, 'sam'])])
		r_file = '/'.join(['/data2', project, 'fastq', i, s, '_'.join([s, date, 'aligned_sorted.bam'])])
		log = '/'.join(['/data2', project, 'HISAT2/outputs', i, s, '_'.join([s, 'hisat', date, 'log.txt'])])
		cmd = []
		cmd.append(' '.join(["hisat2", '-q',
			"-p", "8",
			'_'.join(["--rg-id=" + i, s]),
			'--rg', "SM:" + s,
			'-x', index,
			'--dta',
			'--rna-strandness', 'RF',
			'-1', R1,
			'-2', R2,
			'-S', o_file, '2>', log]))
		cmd.append(' '.join(['samtools', 'sort', '-@', '8', '-o', r_file, o_file, '2>>', log]))
		cmd.append('rm '+o_file)

		cmds.append(cmd)

def mlt_line(commands):
	start = time.time()
	for x in commands:
		print(x)
		os.system(x)
	print('duration time: ', time.time() - start, 'sec')

number_threads = 8

pool = mp.Pool(number_threads)
pool.map(mlt_line, cmds)
pool.close()
pool.join()
