#!/usr/bin/env python3

#This file is part of Mutational Signatures Project.

#Mutational Signatures Project: need info on project

#Copyright (C) 2018 Erik Bergstrom

#

#Mutational Signatures is free software: need to include distribtution

#rights and so forth

#

#Mutational Signatures is distributed in the hope that it will be useful,

#but WITHOUT ANY WARRANTY; without even the implied warranty of

#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

#GNU General Public License for more details [change to whatever group we should include.
 

#Author: Erik Bergstrom

#Contact: ebergstr@eng.ucsd.edu

import os
import sys
import re
import subprocess
import argparse

def install_chromosomes (genomes, custom):
	if custom:
		for genome in genomes:
			os.system("gunzip references/chromosomes/fasta/" + genome + "/*.gz")
			chromosome_fasta_path = "references/chromosomes/fasta/" + genome + "/"
			os.system("python3 scripts/save_chrom_strings.py -g " + genome)
			print("Chromosome string files for " + genome + " have been created. Continuing with installation.")
			#os.system("rm -r " + chromosome_fasta_path)
	else:

		for genome in genomes:
			species = None
			chrom_number = None
			if genome == 'GRCh37' or genome == 'GRCh38': 
				species = "homo_sapiens"
				chrom_number = 24
			elif genome == 'mm10' or genome == 'mm9':
				species = "mus_musculus"
				chrom_number = 21
			else:
				print(genome + " is not supported. The following genomes are supported:\nGRCh37, GRCh38, mm10")
			
			chromosome_string_path = "references/chromosomes/chrom_string/" + genome + "/"
			chromosome_fasta_path = "references/chromosomes/fasta/" + genome + "/"

			wget_flag = True
			if os.path.exists(chromosome_string_path) == False or len(os.listdir(chromosome_string_path)) <= chrom_number:
				if os.path.exists(chromosome_fasta_path) == False or len(os.listdir(chromosome_fasta_path)) <= chrom_number:
					print("Chromosomes are not currently saved as individual text files for " + genome + ". Downloading the files now...")
					try:
						p = subprocess.Popen("wget", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					except:
						proceed = input("You may not have wget or homebrew installed. Download those dependencies now?[Y/N]").upper()
						if proceed == 'Y':
							try:
								os.system("brew install wget")
							except:
								os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
								os.system("brew install wget")
						else:
							print("Installation has stopped. Please download the chromosome files before proceeding with the installation.")
							wget_flag = False
							sys.exit()
					if wget_flag:
						try:
							if genome == 'GRCh37':
								os.system("wget -r -l1 -c -nc --no-parent -A '*.dna.chromosome.*' -nd -P " + chromosome_fasta_path + " ftp://ftp.ensembl.org/pub/grch37/update/fasta/homo_sapiens/dna/")
							elif genome == 'mm9':
								os.system("wget -r -l1 -c -nc --no-parent -A '*.dna.chromosome.*' -nd -P " + chromosome_fasta_path + " ftp://ftp.ensembl.org/pub/release-67/fasta/mus_musculus/dna/")
							else:
								os.system("wget -r -l1 -c -nc --no-parent -A '*.dna.chromosome.*' -nd -P " + chromosome_fasta_path + " ftp://ftp.ensembl.org/pub/release-93/fasta/"+species+"/dna/")
							os.system("gunzip references/chromosomes/fasta/" + genome + "/*.gz")
						except:
							print("The ensembl ftp site is not currently responding.")
							sys.exit()

				print("Chromosome fasta files for " + genome + " have been installed. Creating the chromosome string files now...")
				os.system("python3 scripts/save_chrom_strings.py -g " + genome)
				print("Chromosome string files for " + genome + " have been created. Continuing with installation.")
				os.system("rm -r " + chromosome_fasta_path)

			else:
				print("Chromosome reference files exist for " + genome + ". Continuing with installation.")


def install_chromosomes_tsb (genomes, custom):
	for genome in genomes:
		chrom_string_path = "references/chromosomes/chrom_string/" + genome + "/"
		chrom_number = len(chrom_string_path)

#		if genome == 'mm10':
#			chrom_number = 21
		chromosome_TSB_path = "references/chromosomes/tsb/" + genome + "/"
		transcript_files = "references/chromosomes/transcripts/" + genome + "/"

		if os.path.exists(transcript_files) == False or len(os.listdir(transcript_files)) < 1:
			print("Please download the transcript files before proceeding. You can download the files from 'http://www.ensembl.org/biomart/martview'.")
			print("Follow the format presented in the README file:\n\n\tGene stable ID  Transcript stable ID    Chromosome/scaffold name    Strand  Transcript start (bp)   Transcript end (bp)\n\n\n")
			sys.exit()
		if os.path.exists(chromosome_TSB_path) == False or len(os.listdir(chromosome_TSB_path)) < chrom_number:
			print("The transcriptional reference data for " + genome + " has not been saved. Creating these files now")
			os.system("python3 scripts/save_tsb_192.py -g " + genome)

		print("The transcriptional reference data for " + genome + " has been saved.")





def main ():

	genomes = ['mm9', 'mm10','GRCh37', 'GRCh38' ]
	custom = False
	parser = argparse.ArgumentParser(description="Provide the necessary arguments to install the reference files.")
	parser.add_argument("-g", "--genome", nargs='?', help="Optional parameter instructs script to install the custom genome.")
	args = parser.parse_args()

	if args.genome:
		genomes = [args.genome]


	ref_dir = "references/"
	chrom_string_dir = ref_dir + "chromosomes/chrom_string/"
	chrom_fasta_dir = ref_dir + "chromosomes/fasta/"
	chrom_tsb_dir = ref_dir + "chromosomes/tsb/"
	matrix_dir = ref_dir + "matrix/"
	vcf_dir = ref_dir + "vcf_files/"
	bed_dir = ref_dir + "vcf_files/BED/"
	new_dirs = [ref_dir, chrom_string_dir, chrom_fasta_dir, chrom_tsb_dir, matrix_dir, vcf_dir, bed_dir]

	current_dir = os.getcwd()
	for dirs in new_dirs:
		if not os.path.exists(dirs):
			os.makedirs(dirs)

	initial_transcripts = os.listdir("transcripts_original/")
	for file in initial_transcripts:
		name = file.split("_")
		if not os.path.exists("references/chromosomes/transcripts/"+name[0]+"/"):
			os.makedirs("references/chromosomes/transcripts/"+name[0]+"/")
		if name != ".DS":
			os.system("cp transcripts_original/"+file +" references/chromosomes/transcripts/" + name[0]+"/")

	if os.path.exists("exome/"):
		os.system("mv exome/ references/chromosomes/")

	install_chromosomes(genomes, custom)
	install_chromosomes_tsb (genomes, custom)
	if os.path.exists("BRCA_example/"):
		os.system("mv BRCA_example/ references/vcf_files/")
	if os.path.exists("example_test"):
		os.system("mv example_test/ references/vcf_files/")
	print ("Please place your vcf files for each sample into the 'references/vcf_files/[test]/[mutation_type]/' directory. Once you have done that, you can proceed with the matrix generation.")
	print("Installation complete.")


if __name__ == '__main__':
	main()