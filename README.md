# Nextflow QC Pipeline for Sequencing Runs  

## Overview  
This Nextflow pipeline assesses the success of sequencing runs performed by our core sequencing team. It evaluates the quality and integrity of sequencing data, ensuring they meet the criteria for downstream analyses. The pipeline focuses on two key aspects:
1. Ensuring sufficient quality data for downstream analysis.
2. Verifying successful sequencing of the target organism.  

The pipeline accomplishes these goals by generating mapping-based and assembly-based statistics to comprehensively evaluate sequencing performance.  

---

## Pipeline Workflow  
### **1. Map Raw Reads to Reference Genome**  
- Aligns raw sequencing reads to a provided reference genome.  
- Produces BAM files for subsequent analysis.

### **2. Calculate Mapping-Based Statistics**  
- Computes metrics such as:  
  - **Average Depth of Coverage**: Indicates the quantity of sequencing data. Target: ≥ 20 (context-dependent).  
  - **Percentage of the Genome Covered**: Evaluates how much of the reference genome is covered at specific depths.  
  - **Total Reads Mapped & Percentage of Reads Mapped**: Determines sequencing accuracy for the target organism. Successful runs have >90% reads mapped.  

### **3. Perform De Novo Assembly**  
- Assembles raw reads without reference guidance.  
- Generates FASTA files for contigs.  

### **4. Compute Assembly-Based Statistics**  
- Evaluates the quality of assemblies with metrics such as:  
  - **Total Assembly Length**: Should approximate the expected genome size.  
  - **Number of Contigs**: Fewer contigs indicate better assemblies with fewer gaps.  
  - **N50**: Higher values suggest better contiguity and completeness of assemblies.  

---

## Key Features  

### Mapping-Based Metrics  
- **Average Depth of Coverage**: Ensures sufficient sequencing data.  
- **Percentage of Reads Mapped**: Validates sequencing success for the intended organism.  

### Assembly-Based Metrics  
- **Total Assembly Length**: Validates genome size.  
- **Number of Contigs**: Evaluates assembly completeness.  
- **N50**: Assesses assembly contiguity.  

---

## Requirements  
- **Nextflow**: Workflow orchestration.  
- **Dependencies**:  
  - `bwa` for read mapping.  
  - `samtools` for BAM file manipulation and statistics.  
  - `spades` or similar assembler for de novo assembly.  
  - `QUAST` for assembly evaluation.  

---

## Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-org/qc-pipeline.git
   cd qc-pipeline
   ```  
2. Install dependencies via `conda` or your package manager.  

3. Run the pipeline with:  
   ```bash
   nextflow run main.nf --reads '<path_to_reads>' --reference '<path_to_reference>'
   ```  

---

## Input Parameters  
- `--reads`: Path to raw sequencing reads (FASTQ format).  
- `--reference`: Path to the reference genome (FASTA format).  

---

## Output  
1. **Mapping Results**  
   - BAM files and summary statistics (e.g., coverage, percentage mapped).  

2. **Assembly Results**  
   - FASTA files of contigs.  
   - Assembly evaluation metrics (e.g., N50, total length, number of contigs).  

---

## Contact  
For any issues or questions, please contact Belson Kutambe at `bdkutambe@gmail.com`.  

---  
