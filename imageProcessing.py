from clip_interrogator import Config, Interrogator
import torch

config = Config()
config.device = 'cuda' if torch.cuda.is_available() else 'cpu'
config.blip_offload = False if torch.cuda.is_available() else True
config.chunk_size = 2048
config.flavor_intermediate_count = 512
config.blip_num_beams = 64
ci = Interrogator(config)

def inference(image, mode , best_max_flavors):
    image = image.convert('RGB')
    if mode == 'best':
        
        prompt_result = ci.interrogate(image, max_flavors=int(best_max_flavors))
        
        print("mode best: " + prompt_result)
        
        return prompt_result
    
    elif mode == 'classic':
        
        prompt_result = ci.interrogate_classic(image)
        
        print("mode classic: " + prompt_result)
        
        return prompt_result
    
    else:
        
        prompt_result = ci.interrogate_fast(image)
        
        print("mode fast: " + prompt_result)
        
        return prompt_result