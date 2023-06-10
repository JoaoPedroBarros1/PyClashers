

class Heroi:
    nome = "Peter Parker"
    voa = False
    possui_arma = False
    lanca_teia = False
    frase_comum = ""

    def falar(self):
        print(self.frase_comum)

    def detalhar(self):
        if self.voa:
            print(f"O {self.nome} voa.")
        if self.possui_arma:
            print(f"O {self.nome} possui arma.")
        if self.lanca_teia:
            print(f"O {self.nome} lança teia.")


homem_aranha = Heroi()
homem_aranha.lanca_teia = True
print(homem_aranha.voa)
print(homem_aranha.lanca_teia)

he_man = Heroi()
he_man.possui_arma = True
he_man.lanca_teia = False
he_man.voa = False
he_man.frase_comum = "Eu tenho a força"
he_man.falar()
homem_aranha.detalhar()
he_man.detalhar()
