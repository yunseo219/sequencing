import os, sys, json
import glob
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
import time
project = 'P_diamond_pilot'
date = '20201202'

start = time.time()
f = open('/data2/'+ project + '/outputs/Tables/' + project + '_table.json', "r")
samples = json.load(f)
f.close()

index ='/data2/P_diamond_pilot'
GTF = '/data2/P_diamond_pilot/gencode.v32.primary_assembly.annotation.gtf'
cmds = []

for i in samples.keys():
	pwd = '/data2/P_diamond_pilot/fastq/' + i +'/'
	print('/'.join(['mkdir /data2', project, 'fastq', i]))
	os.system('/'.join(['mkdir /data2', project, 'fastq', i]))
	for s in samples[i]:
		print('/'.join(['mkdir /data2', project, 'fastq', i, s]))
		os.system('/'.join(['mkdir /data2', project, 'fastq', i, s]))
		R1 = glob.glob(pwd + s + '*R1*')[0]
		R2 = glob.glob(pwd + s + '*R2*')[0]
		o_folder = '_'.join(['/'.join(['/data2', project, 'fastq', i, s]), s, date, ''])
		ID = r'\t'.join(['_'.join(['ID:'+i, s]), '_'.join(['SM:'+s])])

		cmd = ' '.join(['STAR',
			'--readFilesIn', R1, R2,
			'--outSAMattrRGline', ID,
			'--alignIntronMax', '1000000',
			'--alignIntronMin', '20',
			'--alignMatesGapMax', '1000000',
			'--alignSJDBoverhangMin', '1',
			'--alignSJoverhangMin', '8',
			'--alignSoftClipAtReferenceEnds', 'Yes',
			'--chimJunctionOverhangMin', '15',
			'--chimMainSegmentMultNmax', '1',
			'--chimOutType', 'Junctions SeparateSAMold WithinBAM SoftClip',
			'--chimSegmentMin', '15',
			'--genomeDir', index,
			'--genomeLoad', 'NoSharedMemory',
			'--limitSjdbInsertNsj', '1200000',
			'--outFileNamePrefix', o_folder,
			'--outFilterIntronMotifs', 'None',
			'--outFilterMatchNminOverLread', '0.33',
			'--outFilterMismatchNmax', '999',
			'--outFilterMismatchNoverLmax', '0.1',
			'--outFilterMultimapNmax', '20',
			'--outFilterScoreMinOverLread', '0.33',
			'--outFilterType', 'BySJout',
			'--outSAMattributes', 'NH HI AS nM NM ch',
			'--outSAMstrandField', 'intronMotif',
			'--outSAMtype', 'BAM Unsorted',
			'--outSAMunmapped', 'Within',
			'--quantMode', 'TranscriptomeSAM GeneCounts',
			#'--readFilesCommand', 'zcat',
			'--runThreadN', '8',
			#'--sjdbGTFfile', GTF, # not included in TCGA pipeline
			#'--sjdbOverhang', '150', # not included in TCGA pipeline
			'--twopassMode', 'Basic'])
		cmds.append(cmd)

def mlt_line(x):
    start_tmp = time.time()
    print(x)
    os.system(x)
    print("time :", time.time() - start_tmp, "sec")

number_threads = 5

pool = mp.Pool(number_threads)
pool.map(mlt_line, cmds )
pool.close()
pool.join()

print("time :", time.time() - start, "sec")
