import os
import torch
from tqdm import tqdm
import torch.nn as nn

def train_bert(train_loader, test_loader, bert_model, optimizer, criterion, scheduler, log_file, ckpt_path):
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    f = open(f"{log_file}", "a")

    for epoch in range(1, 11):
        total_train_loss = 0.0
        total_test_loss = 0.0

        total_train_acc = 0
        total_test_acc = 0
    
        # Traina
        bert_model.train()
        best_loss = float('inf')
        acc = []

        scheduler.step()

        with tqdm(train_loader, unit="batch") as t_epoch:
            for batch in t_epoch:
                t_epoch.set_description(f"Training at Epoch {epoch}")
                data, label, mask = batch
                data = data.squeeze(1).to(device)
                label = label.to(device)
                mask = mask.to(device)

                optimizer.zero_grad()
                output = bert_model(data, attention_mask=mask)
                loss = criterion(output, label)

                pred = torch.max(output, dim=1)[1]
                total_train_acc += (pred == label).to(torch.float).mean()

                loss.backward()
                optimizer.step()

                total_train_loss += loss.item()
                t_epoch.set_postfix(loss=loss.item(), accuracy= 100*float((pred == label).to(torch.float).mean()))
                
        average_train_loss = total_train_loss / len(train_loader)
        average_train_acc = total_train_acc / len(train_loader)

        print('\nEpoch {}: Avg. Train Loss: {:.4f}'.format(epoch, average_train_loss))
        print('Epoch {}: Avg. Train Acc.: {:.4f}'.format(epoch, average_train_acc))
        
        # Test
        bert_model.eval()

        with torch.no_grad():
            with tqdm(test_loader, unit="batch") as v_epoch:
                for batch in v_epoch:
                    v_epoch.set_description(f"Testing at Epoch {epoch}")
                    data, label, mask = batch
                    data = data.squeeze(1).to(device)
                    label = label.to(device)
                    mask = mask.to(device)

                    output = bert_model(data, attention_mask=mask)
                    loss = criterion(output, label)

                    pred = torch.max(output, dim=1)[1]
                    total_test_acc += (pred == label).to(torch.float).mean()

                    total_test_loss += loss.item()
                    v_epoch.set_postfix(loss=loss.item(), accuracy= 100*float((pred == label).to(torch.float).mean()))

            average_test_loss = total_test_loss / len(test_loader)
            average_test_acc = total_test_acc / len(test_loader)

        acc.append(average_test_acc)
        print('\nEpoch {}: Avg. Test Loss: {:.4f}'.format(epoch, average_test_loss))
        print('Epoch {}: Avg. Test Acc.: {:.4f}'.format(epoch, average_test_acc))

        ## Saving
        ckpt = {'model': bert_model.state_dict(),
                'optimizer': optimizer.state_dict(),
                'epoch': epoch,
                'train_loss': average_train_loss,
                'test_loss': average_test_loss,
                }

        torch.save(ckpt, f"{ckpt_path}/bert-last.pth")

        if average_test_loss < best_loss:
            best_loss = average_test_loss
            torch.save(ckpt, f"{ckpt_path}/bert-best.pth")

        f.write('Epoch {}: Avg. Train Loss: {:.4f}\n'.format(epoch, average_train_loss))
        f.write('Epoch {}: Avg. Train Acc.: {:.4f}\n'.format(epoch, average_train_acc))
        f.write('Epoch {}: Avg. Test Loss: {:.4f}\n'.format(epoch, average_test_loss))
        f.write('Epoch {}: Avg. Test Acc.: {:.4f}\n\n'.format(epoch, average_test_acc))
        f.flush()
