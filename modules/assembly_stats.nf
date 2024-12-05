nextflow.enable.dsl=2

// Assemble the raw reads 

process assemble {
    label 'spades'
    publishDir "${params.outdir}/${sample}", mode: "copy"

    input:
    tuple val(sample),path(fastq) //unpacking 

    output:
    tuple val(sample),path("${sample}_assembly")

    shell:
    fastqs = "${fastq[0]} ${fastq[1]}"
    '''
    spades.py -1 !{fastq[0]}  -2 !{fastq[1]}  -o !{sample}_assembly
    '''
}

// Calculate assembly stats

process assembly_stats {
    label 'quast'
    publishDir "${params.outdir}/${sample}", mode: "copy"
    input:
    tuple val(sample),path(assembly)

    output:
    tuple val(sample),path("${sample}_quast")

    shell:
    '''
    quast !{assembly} -o !{sample}_quast
    '''
}

// Merge quast results for all samples
process merge_quast {
   publishDir "${params.outdir}", mode: "copy"

    input:
    tuple val(sample),path(stats)

    output:
    stdout

    shell:
    '''
    if [[ ! -e "!{params.outdir}/assembly_stats.csv" ]]; then
        echo "Sample,total_contig,total_contig_length,n50_contig_length" > "!{params.outdir}/assembly_stats.csv"
    fi

    cut -f 1,2,3,8 !{stats}/report.tsv >> !{params.outdir}/assembly_stats.csv
    '''
}

workflow {
    samples_ch = Channel.fromFilePairs(params.samples)
    
    assemble(samples_ch)
    assembly_stats(assemble.out)
    merge_quast(assembly_stats.out)
    
}
