import torch
from tqdm import tqdm
import os
import pandas as pd
tqdm.pandas()
from transformers import GPT2Tokenizer
from gpt2 import GPT2HeadWithValueModel, respond_to_batch 
import datetime
import argparse
os.environ["CUDA_VISIBLE_DEVICES"] = '6'

parser = argparse.ArgumentParser(description="")
parser.add_argument('--lm_name')
parser.add_argument('--ref_lm_name')
parser.add_argument('--total_nums')
parser.add_argument('--txt_in_len')
parser.add_argument('--txt_out_len')
parser.add_argument('--savePath')
args = parser.parse_args()

lm_name = args.lm_name
ref_lm_name = args.ref_lm_name
total_nums = int(args.total_nums)
txt_in_len=int(args.txt_in_len)
txt_out_len=int(args.txt_out_len)
savePath=args.savePath
tokenizer = gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
gpt2_model = GPT2HeadWithValueModel.from_pretrained(lm_name)
gpt2_model_ref = GPT2HeadWithValueModel.from_pretrained(ref_lm_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_ = gpt2_model.eval()
_ = gpt2_model.to(device)
_ = gpt2_model_ref.eval()
_ = gpt2_model_ref.to(device)

bs = 64
wafData=pd.DataFrame()
wafData['content']=['0' for _ in range(30000)]
wafData['tokens']=wafData['content'].progress_apply(lambda x: gpt2_tokenizer.encode(x, return_tensors="pt").to(device)[0, :txt_in_len])
wafData['query'] = wafData['tokens'].progress_apply(lambda x: gpt2_tokenizer.decode(x))


responseList=[]

starttime = datetime.datetime.now()
while len(responseList)<total_nums:
    torch.cuda.empty_cache()
    df_batch = wafData.sample(bs)
    query_tensors = torch.stack(df_batch['tokens'].tolist())
    response_tensors = respond_to_batch(gpt2_model, gpt2_model_ref, query_tensors, txt_len=txt_out_len)
    responseList+= [gpt2_tokenizer.decode(response_tensors[i, :]).split('!')[0] for i in range(bs)]
endtime = datetime.datetime.now()
print((endtime - starttime).seconds)

df_results = pd.DataFrame()

df_results['response']=responseList
df_results['query']='0'
df_results['data']=df_results['query']+df_results['response']
df_results[['data']].to_csv(savePath,index=False)


