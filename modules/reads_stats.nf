nextflow.enable.dsl=2

// map raw reads to the reference genome

process bwa_mem {
    publishDir "${params.outdir}/${sample}", mode: "copy"

    input:
    tuple val(sample),path(fastq)
    each path(reference)

    output:
    tuple val(sample),path("${sample}.sam")

    shell:
    fastqs = "${fastq[0]} ${fastq[1]}"
    '''
    bwa index !{reference}
    bwa mem !{reference} !{fastqs} > !{sample}.sam
    '''
}

// Convert sam file to bam

process sam_2_bam {
    publishDir "${params.outdir}/${sample}", mode: "copy"
    input:
    tuple val(sample),path(sam)

    output:
    tuple val(sample),path("${sample}.bam")

    shell:
    '''
    samtools view -S -b !{sam} > !{sample}.bam
    '''
}

// Sort the bam
process sort_bam {
    publishDir "${params.outdir}/${sample}", mode: "copy"
    input:
    tuple val(sample),path(bam)

    output:
    tuple val(sample),path("${sample}.sorted.bam")

    shell:
    '''
    samtools sort -o !{sample}.sorted.bam !{bam}
    '''
}

//Index the bam
process index_bam {
    publishDir "${params.outdir}/${sample}", mode: "copy"
    input:
    tuple val(sample),path(sorted_bam)

    output:
    tuple val(sample),path('*.bai')

    shell:
    '''
    samtools index !{sorted_bam}
    '''
}

// samtools depth
process samtools_depth {
    publishDir "${params.outdir}/${sample}", mode: "copy"
    input:
    tuple val(sample),path(sorted_bam)

    output:
    tuple val(sample),path("${sample}.coverage.txt")

    shell:
    '''
    samtools depth -aa !{sorted_bam} > !{sample}.coverage.txt
    '''
}

// samtools flagstat
process samtools_flagstat {
    publishDir "${params.outdir}/${sample}", mode: "copy"
    input:
    tuple val(sample),path(sorted_bam)

    output:
    tuple val(sample),path("${sample}.cov_prop.txt")

    shell:
    '''
    samtools flagstat !{sorted_bam} > !{sample}.cov_prop.txt
    '''
}

// extractions
process extract {
    publishDir "${params.outdir}/${sample}", mode: "copy"
    
    input:
    tuple val(sample),path(coverage)
    tuple val(sample),path(proportion)

    output:
    tuple val(sample),path("${sample}.seq_stats.csv")

    shell:
    """
    echo "Sample,Avg_depth,perc_cov_10x,perc_cov_30x,total_reads,reads_mapped,reads_mapped_percentage" > !{sample}.seq_stats.csv
    avg=\$(awk '{sum+=\$3} END {if (NR > 0) print sum/NR; else print "0"}' !{coverage})
    tenx=\$(awk '\$3 >= 10 {sum+=1} END {if (NR > 0) print (sum / 3935232) * 100; else print "0"}' !{coverage})
    thirtyx=\$(awk '\$3 >= 30 {sum+=1} END {if (NR > 0) print (sum / 3935232) * 100; else print "0"}' !{coverage})
    
    # Extract total reads
    total_reads=\$(grep -Eo '^[0-9]+ \\+ 0 in total' !{proportion} | awk '{print \$1}')

    # Extract total reads mapped
    total_mapped=\$(grep -Eo '^[0-9]+ \\+ 0 mapped' !{proportion} | awk '{print \$1}')

    # Extract reads mapped percentage without '('
    mapped_percentage=\$(grep -Eo '^[0-9]+ \\+ 0 mapped \\([0-9.]+%' !{proportion} | awk '{gsub("%", ""); gsub("\\(", ""); print \$NF}')
    
    echo "!{sample},\$avg,\$tenx,\$thirtyx,\$total_reads,\$total_mapped,\$mapped_percentage" >> !{sample}.seq_stats.csv
    """
}




process concatenate {
    publishDir "${params.outdir}", mode: "copy"

    input:
    tuple val(sample),path(stats)

    output:
    stdout

    shell:
    '''
    if [[ ! -e "!{params.outdir}/seq_stats.csv" ]]; then
        echo "Sample,Avg_depth,perc_cov_10x,perc_cov_30x,total_reads,reads_mapped,reads_mapped_percentage" > "!{params.outdir}/seq_stats.csv"
    fi

    sed -n '2p' "!{stats}" >> "!{params.outdir}/seq_stats.csv"
    '''
}


workflow {
    samples_ch = Channel.fromFilePairs(params.samples)
    ref_ch = Channel.fromPath(params.ref)
    

    bwa_mem(samples_ch,ref_ch)
    sam_2_bam(bwa_mem.out)
    sort_bam(sam_2_bam.out)
    index_bam(sort_bam.out)
    samtools_depth(sort_bam.out)
    samtools_flagstat(sort_bam.out)
    extract(samtools_depth.out,samtools_flagstat.out)
    concatenate(extract.out)
}
