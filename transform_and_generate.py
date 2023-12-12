#! /usr/bin/env python3

# Irfansha Shaik, Aarhus, 12 December 2023.

import sys
import os, subprocess
import time




if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description="Transform a QCIR to QDIMACS and generate a certificate in CNF")
    parser.add_argument("-i", "--input", help="input file (in QCIR format), default 'benchmarks/conditional.qcir'", default = "benchmarks/conditional.qcir")
    parser.add_argument("--out_qdimacs", help="output circuit file (in QDIMACS format), default 'intermediate_files/conditional.qdimacs'", default = "intermediate_files/conditional.qdimacs")
    parser.add_argument("--out_cert", "--output", help="output file (in aag format), default 'intermediate_files/conditional.aag'", default = "intermediate_files/conditional.aag")
    parser.add_argument("-t", "--time_limit",type=int, help="time limit in seconds, default 300s", default = 300)


    args = parser.parse_args()
    
    #print(args.input)

    # Transform QCIR input to QDIMACS:
    transform = 'python3 qcir_to_qdimacs_transformer.py --input_file ' + args.input + ' --output_file ' + args.out_qdimacs
    print(transform)
    os.system(transform)

    # Generate aag certificate:
    # first generating the qrp trace:
    command = "./solvers/depqbf/depqbf --trace " + args.out_qdimacs + " > intermediate_files/depqbf_qrp_trace.qrp"
    print(command)
    try:
      subprocess.run([command], shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT ,check=True, timeout=args.time_limit)
    except subprocess.TimeoutExpired:
      print("Time out after " + str(args.time_limit)+ " seconds.")
    except subprocess.CalledProcessError as e:
      # 10, 20 are statuses for SAT and UNSAT:
      if ("exit status 10" not in str(e) and "exit status 20"  not in str(e)):
        print("Error from solver :", e, e.output)

      cert_generation_command = "./qrpcert/qrpcert --aiger-ascii --simplify intermediate_files/depqbf_qrp_trace.qrp > " + args.out_cert
      print(cert_generation_command)
      # this must be very light process no need of time limit:
      os.system(cert_generation_command)