import torch
import torch.nn as nn
import torch.nn.functional as F
import transformers
# assert transformers.__version__ == '2.8.0'
from transformers import GPT2Config, GPT2Tokenizer, GPT2Model

# Define the generator model
class Generator(nn.Module):
    def __init__(self, gpt, config, max_len=31):
        super(Generator, self).__init__()
        self.gpt = gpt
        self.config = config
        self.max_len = max_len
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

    def forward(self, inputs):
        # input: [batch, seq]
        context_len = inputs.size(1)
        generated = inputs
        next_token = inputs
        past = None
        with torch.no_grad():
            for step in range(self.max_len):
                outputs = self.gpt(next_token, past=past)
                hidden = outputs[0][:, -1]
                past = outputs[1]
                next_token_logits = self.lm_head(hidden)
                next_logits, next_token = next_token_logits.topk(k=1, dim=1)
                generated = torch.cat((generated, next_token), dim=1)
        return generated 

def prepare_input(head_entity, tail_entity, tokenizer, input_len=16 ):
    head_entity = head_entity.replace('_', ' ')
    tail_entity = tail_entity.replace('_', ' ')
    input_token = tail_entity + '<SEP>' + head_entity
    input_id = tokenizer.encode(input_token, add_special_tokens=False)[:input_len]
    input_id += [tokenizer.convert_tokens_to_ids('<PAD>')] * (input_len - len(input_id))
    return torch.tensor([input_id], dtype=torch.long)

def connect_entities(head_entity, tail_entity, tokenizer, generator):
    gen_input = prepare_input(head_entity, tail_entity, tokenizer)
    gen_output = generator(gen_input)
    path = tokenizer.decode(gen_output[0].tolist(), skip_special_tokens=True)
    path = ' '.join(path.replace('<PAD>', '').split())
    return path[path.index('<SEP>')+6:]


import argparse

def main():
    parser = argparse.ArgumentParser(description='Set the model file path')
    parser.add_argument('--pretrained_model_path', type=str, default=None, help='pretrained path generator model path')

    args = parser.parse_args()

    # load pretrained path generator
    print("pretrained model loading...")
    lm_type = 'gpt2'
    config = GPT2Config.from_pretrained(lm_type)
    tokenizer = GPT2Tokenizer.from_pretrained(lm_type)
    tokenizer.add_tokens(['<PAD>'])
    tokenizer.add_tokens(['<SEP>'])
    tokenizer.add_tokens(['<END>'])
    gpt = GPT2Model.from_pretrained(lm_type)
    config.vocab_size = len(tokenizer)
    gpt.resize_token_embeddings(len(tokenizer))

    generator = Generator(gpt, config)
    generator.load_state_dict(torch.load(args.pretrained_model_path, map_location='cpu'))  

    flag = True
    while flag:
        try:
            head_ent = input('Type head entity : ') 
            tail_ent = input('Type tail entity : ')
            path = connect_entities(head_ent, tail_ent, tokenizer, generator)    
            print('path generated by PG : {}'.format(path))  
        except EOFError:
            break 


if __name__ == '__main__':
    main()