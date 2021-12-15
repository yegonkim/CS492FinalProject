import os
from tqdm import tqdm
import torch

def train_MM(train_loader, test_loader, mm_model, optimizer, criterion, scheduler, exp_name, ckpt_path):

    f = open(f"{exp_name}.txt", "a")

    for epoch in range(1, 51):
        total_train_loss = 0.0
        total_test_loss = 0.0

        total_train_acc = 0
        total_test_acc = 0
    
        # Train
        mm_model.train()
        best_loss = float('inf')
        acc = []

        scheduler.step()
        optimizer.zero_grad()

        with tqdm(train_loader, unit="batch") as t_epoch:
            for idx, batch in enumerate(t_epoch):
                t_epoch.set_description(f"Training at Epoch {epoch}")

                speech, length, text, mask, label = batch
                speech = speech.transpose(1, 0).to("cuda")
                length = length.to("cuda")
                text = text.to("cuda")
                mask = mask.to("cuda")
                label = label.to("cuda")

                with torch.set_grad_enabled(True):
                    output = mm_model(speech, length, text, mask)
                    loss = criterion(output, label)

                    pred = torch.max(output, dim=1)[1]
                    total_train_acc += (pred == label).to(torch.float).mean().detach().item()

                    loss.backward()
                
                    if (idx + 1) % 8 ==0:
                        optimizer.step()            
                        optimizer.zero_grad()

                    total_train_loss += loss.item()
                    t_epoch.set_postfix(loss=loss.item(), accuracy= 100*(pred == label).to(torch.float).mean().detach().item())

        
        average_train_loss = total_train_loss / len(train_loader)
        average_train_acc = total_train_acc / len(train_loader)

        print('\nEpoch {}: Avg. Train Loss: {:.4f}'.format(epoch, average_train_loss))
        print('Epoch {}: Avg. Train Acc.: {:.4f}'.format(epoch, average_train_acc))
        

        # # # Test
        optimizer.zero_grad()
        mm_model.eval()

        if epoch > 0:
            with torch.no_grad():
                with tqdm(test_loader, unit="batch", position=0, leave=True) as v_epoch:
                    for batch in v_epoch:
                        v_epoch.set_description(f"Testing at Epoch {epoch}")
                        speech, length, text, mask, label = batch

                        speech = speech.transpose(1, 0).to("cuda")
                        length = length.to("cuda")
                        text = text.squeeze(1).to("cuda")
                        mask = mask.to("cuda")
                        label = label.to("cuda")

                        output = mm_model(speech, length, text, mask)
                        loss = criterion(output, label)

                        pred = torch.max(output, dim=1)[1]
                        total_test_acc += (pred == label).to(torch.float).mean().item()

                        total_test_loss += loss.item()
                        v_epoch.set_postfix(loss=loss.item(), accuracy= 100*float((pred == label).to(torch.float).mean().item()))
            
        average_test_loss = total_test_loss / len(test_loader)
        average_test_acc = total_test_acc / len(test_loader)

        acc.append(average_test_acc)
        print('\nEpoch {}: Avg. Test Loss: {:.4f}'.format(epoch, average_test_loss))
        print('Epoch {}: Avg. Test Acc.: {:.4f}'.format(epoch, average_test_acc))

        ## Saving
        ckpt = {'model': mm_model.state_dict(),
                'optimizer': optimizer.state_dict(),
                'epoch': epoch
                }

        torch.save(ckpt, os.path.join(ckpt_path, f"{exp_name}-last.pth"))

        if average_test_loss < best_loss:
            best_loss = average_test_loss
            torch.save(ckpt, os.path.join(ckpt_path, f"{exp_name}-best.pth"))

        f.write('Epoch {}: Avg. Train Loss: {:.4f}\n'.format(epoch, average_train_loss))
        f.write('Epoch {}: Avg. Train Acc.: {:.4f}\n'.format(epoch, average_train_acc))
        f.write('Epoch {}: Avg. Test Loss: {:.4f}\n'.format(epoch, average_test_loss))
        f.write('Epoch {}: Avg. Test Acc.: {:.4f}\n\n'.format(epoch, average_test_acc))
        f.flush()
