import subprocess, glob, json, re

project = 'P_diamond_pilot'
i_dir = '/data2'
o_dir = '/data2/P_diamond_pilot/outputs'
dir_num = len(i_dir.split('/'))

list_family = glob.glob('/'.join([i_dir, project, 'fastq', '*']))
fid = {}
for f in list_family:
    fid[f.split('/')[dir_num + 2]] = []

for f in fid.keys():
    list_samples = glob.glob('/'.join([i_dir, project, 'fastq', f, '*fastq']))
    sid = []
    for a in list_samples:
        s = '_'.join(a.split('/')[dir_num + 3].split('_')[0:5])
        if not s in sid:
            sid.append(s)
    fid[f] = sorted(sid)

print("write")
print(fid)

subprocess.run('/'.join(['mkdir ' + o_dir]), shell=True)
subprocess.run('/'.join(['mkdir ' + o_dir, 'Tables']), shell=True)
subprocess.run('/'.join(['mkdir ' + o_dir, 'Figures']), shell=True)

# write json
f = open('/'.join([o_dir, 'Tables', '_'.join([project, 'table.json'])]), "w", newline='')
json.dump(fid, f, indent=2, sort_keys=True)
f.close()

# open json
f = open('/'.join([o_dir, 'Tables', '_'.join([project, 'table.json'])]), "r")
samples = json.load(f)

print("read")
print(samples)
