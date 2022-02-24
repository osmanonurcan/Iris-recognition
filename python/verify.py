##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse
from time import time

from fnc.extractFeature import extractFeature
from fnc.matching import matching


#------------------------------------------------------------------------------
#	Argument parsing
#------------------------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str,
                    help="Path to the file that you want to verify.")

parser.add_argument("--temp_dir", type=str, default="./templates/temp/",
					help="Path to the directory containing templates.")

parser.add_argument("--thres", type=float, default=0.4,
					help="Threshold for matching.")

args = parser.parse_args()


##-----------------------------------------------------------------------------
##  Execution
##-----------------------------------------------------------------------------
# Extract feature
start = time()
print('>>> Start verifying {}\n'.format(args.file))
template, mask, file = extractFeature(args.file)


# Matching
result = matching(template, mask, args.temp_dir, args.thres)

print(type(result))
print(result[0])
if result == -1:
	print('>>> No registered sample.')

elif result == 0:
	print('>>> No sample matched.')

else:
	print('>>> {} samples matched (descending reliability):'.format(len(result)))
	for res in result:
		print("\t", res)


# Time measure
end = time()
print('\n>>> Verification time: {} [s]\n'.format(end - start))