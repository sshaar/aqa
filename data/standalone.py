from allennlp.predictors import Predictor
from allennlp.models.archival import load_archive
from allennlp.common.util import import_submodules, sanitize
import torch
import_submodules('imojie')


def process(token_ids):
    temp=" ".join(token_ids)
    temp = temp.replace(" ##","")
    temp = temp.replace('[unused1]','( ')
    temp = temp.replace('[unused2]',' ; ')
    temp = temp.replace('[unused3]', '')
    temp = temp.replace('[unused4]', ' ; ')
    temp = temp.replace("[unused5]", '')
    temp = temp.replace('[unused6]',' )')
    temp = temp.strip()
    temp = temp.split('[SEP]')
    ans = []
    for x in temp:
        if x != '':
            ans.append(x)
    return ans


if __name__ == '__main__':
    device = 0 if torch.cuda.is_available() else -1
    archive = load_archive(
        "../pretrained_models/imojie",
        weights_file="../pretrained_models/imojie/model_state_epoch_7.th",
        cuda_device=device)

    predictor = Predictor.from_archive(archive, "noie_seq2seq")
    inp_sent = 'England is a country that is part of the United Kingdom, while France is a part of Europe.'
    inp_instance = predictor._dataset_reader.text_to_instance(inp_sent)
    output = predictor._model.forward_on_instance(inp_instance)
    output = sanitize(output)
    output = process(output["predicted_tokens"][0])
    print(output)
