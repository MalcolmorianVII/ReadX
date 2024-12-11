import subprocess
import os

def run_nextflow_pipeline(input_file, output_dir):
    nextflow_cmd = [
        'nextflow', 'run', 'your_pipeline.nf',
        '--input', input_file,
        '--output', output_dir
    ]
    try:
        result = subprocess.run(nextflow_cmd, capture_output=True, text=True, check=True)
        return {'success': True, 'stdout': result.stdout, 'stderr': result.stderr}
    except subprocess.CalledProcessError as e:
        return {'success': False, 'stdout': e.stdout, 'stderr': e.stderr}
