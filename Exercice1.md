# CheckPoint 1
***
***
## Exercice 1
***
***
### Partition 1.1
***
***
![1 1](https://github.com/user-attachments/assets/c922beb2-6e75-450b-b80b-62b333dc4102)
***
![1 3](https://github.com/user-attachments/assets/f0679592-51fd-46de-8220-ecc0b108af87)
***
![1 4](https://github.com/user-attachments/assets/8702e80f-2ece-43dc-b228-3d19ccf099b8)
***
![1 5](https://github.com/user-attachments/assets/12ade30d-598a-47f7-b0a9-08e8744481d8)
***
![1 6](https://github.com/user-attachments/assets/02617da2-a472-400b-b8a3-5e19cde03c1f)
***
![1 7](https://github.com/user-attachments/assets/b81cdd94-04a5-4765-8a06-bf296f2d5031)
***
### Partition 1.2
***
![1 8](https://github.com/user-attachments/assets/f1a7b398-a55f-487a-9705-3fa0fca9ecc3)
***
![1 9](https://github.com/user-attachments/assets/138b87c4-cc32-4098-ae94-a4b00933cefc)
***
![1 10 1](https://github.com/user-attachments/assets/08a4d549-3653-44be-b279-c955f06be6f3)
***
![1 11 2](https://github.com/user-attachments/assets/8853903d-b83f-4b72-97c5-35aaf7dbb523)
***
Ensuite on édite
```nano /etc/fstab```
***
On commente dans le nano : 
#Nouveau point de montage 2ème disque
```UUID="cc871e7d-5158-46d6-b508-89671f30acbc" /mnt/DATA TYPE="ext4" defaults 0 0```
**ctrl + x** suivi de ```Y``` pour enregistrer le nano
***
redémarrage de la VM avec un ```ìnit 6```

