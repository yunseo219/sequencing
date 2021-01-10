import subprocess, json, time
import multiprocessing as mp
from multiprocessing import Pool, cpu_count

project = 'P_diamond_pilot'
date_star = '20201203'
date = '20201211'
#table = '/data2/P_diamond_pilot/outputs'
o_dir = '/data2'
number_threads = 5

start = time.time()
cmds = []
f = open('/data2/'+ project +'/outputs/Tables/'+ project +'_table.json', "r")
samples = json.load(f)
f.close()

gtf = '/data2/P_diamond_pilot/gencode.v32.primary_assembly.annotation.gtf'
cmds = []

for i in samples.keys():
    for s in samples[i]:
        pwd = '/'.join([o_dir, project, 'fastq', i, s, ''])
        bam = '_'.join([pwd +'outputs', s, date_star, 'Aligned.out.bam'])
        inter = '_'.join([pwd +'outputs', s, date, 'SortedByName.out.bam'])
        o_file = '_'.join([pwd +'outputs', s, date, 'strict_Quantified.txt'])
        log = '_'.join([pwd +'outputs', s, date, 'HTseq_quant_log.txt'])
        tmp = '/'.join([pwd, 'tmp'])
        cmd = []
        
        cmd.append(' '.join(['samtools', 'sort',
              '-n', '-T', tmp,
              '-o', inter,
              '-@', '8',
              bam, '2>', log]))
        cmd.append(' '.join(['htseq-count',
              '-f', 'bam',
              '-r', 'name',
              '-s', 'no',
              '-a', '10',
              '-t', 'exon',
              '-i', 'gene_id',
              '-m', 'intersection-strict',
              # '--max-reads-in-buffer', '300000000'
              inter, gtf,
              '>', o_file,
              '2>>', log]))
        cmd.append("rm " + inter)
        cmds.append(cmd)

def mlt_line(x):
    start_tmp = time.time()
    #for i in x:
    print(x)
    subprocess.run(x, shell=True)
    print("time :", time.time() - start_tmp, "sec")

pool = mp.Pool(number_threads)
pool.map(mlt_line, cmds)
pool.close()
pool.join()

print("time :", time.time() - start, "sec")

