nextflow.enable.dsl=2
include  { ; } from './modules/reads_stats'
include { ; } from './modules/assembly_stats'


workflow READS_STATS {
    // do reads based stats
}

workflow ASSEMBLY_STATS {
    // do reads ASSEMBLY  stats
}

workflow {
    // do reads based stats
    // do reads ASSEMBLY  stats

}