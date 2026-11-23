def obter_spread_percentual(valor_reais):
  if valor_reais < 2000:
    return 0.04
  elif valor_reais < 10000:
    return 0.025
  else:
    return 0.015


def obter_aliquota_iof(finalidade):
  if finalidade == "1":
    return 0.035  # 3,5% remessa a conta própria no exterior
  elif finalidade == "2":
    return 0.011  # 1,1% remessa destinada a investimento
  elif finalidade == "3":
    return 0.0038  # 0,38% entrada de recursos
  else:
    return 0.035


def calcular_remessa(valor_reais, finalidade, moeda, cotacao_comercial):
  iof_aliq = obter_aliquota_iof(finalidade)
  spread_aliq = obter_spread_percentual(valor_reais)

  iof_valor = valor_reais * iof_aliq
  liquido_reais = valor_reais - iof_valor
  cotacao_cliente = cotacao_comercial * (1 + spread_aliq)
  valor_estrangeiro = liquido_reais / cotacao_cliente
  vet = valor_reais / valor_estrangeiro if valor_estrangeiro > 0 else 0.0

  return {
      "iof": iof_valor,
      "liquido": liquido_reais,
      "cotacao_cliente": cotacao_cliente,
      "convertido": valor_estrangeiro,
      "vet": vet,
  }


def mostrar_comparativo_investimento(valor_reais, moeda, cotacao_comercial):
  simbolo = "EUR" if moeda == "EUR" else "USD"
  conta_propria = calcular_remessa(valor_reais, "1", moeda, cotacao_comercial)
  investimento = calcular_remessa(valor_reais, "2", moeda, cotacao_comercial)
  diferenca = investimento["convertido"] - conta_propria["convertido"]

  print("\n--- Comparativo: Conta própria (3,5% IOF) vs. Investimento (1,1% IOF) ---")
  print(
      f"Com 3,5% IOF: {conta_propria['convertido']:.2f} {simbolo} | VET:"
      f" R$ {conta_propria['vet']:.4f}"
  )
  print(
      f"Com 1,1% IOF: {investimento['convertido']:.2f} {simbolo} | VET:"
      f" R$ {investimento['vet']:.4f}"
  )
  print(
      f"Diferença a mais na finalidade investimento: +{diferenca:.2f} {simbolo}"
  )


def main():
  print("=== Validador de Remessas Internacionais ===")
  print(
      "Contexto: envio de recursos para França/Europa ou EUA (ex.: livros,"
      " partituras, viagem).\n"
  )

  entrada_valor = input(
      "Valor da remessa em reais (ex.: 1000.00): "
  ).replace(",", ".")
  valor_reais = float(entrada_valor)

  print("\nEscolha a finalidade:")
  print("1 - Remessa a conta própria no exterior (IOF 3,5%)")
  print("2 - Remessa destinada a investimento (IOF 1,1%)")
  print("3 - Entrada de recursos (IOF 0,38%)")
  finalidade = input("Opção (1, 2 ou 3): ").strip()

  print("\nEscolha a moeda de destino:")
  print("EUR - Euro (ex.: planos em Paris / Lyon)")
  print("USD - Dólar americano")
  moeda = input("Moeda (EUR ou USD): ").strip().upper()
  if moeda not in ("EUR", "USD"):
    moeda = "EUR"

  entrada_cotacao = input(
      f"Cotação comercial atual do {moeda} em reais (ex.: 5.60): "
  ).replace(",", ".")
  cotacao_comercial = float(entrada_cotacao)

  resultado = calcular_remessa(valor_reais, finalidade, moeda, cotacao_comercial)

  print("\n=== Resumo da Operação ===")
  print(f"Valor original: R$ {valor_reais:.2f}")
  print(f"IOF descontado: R$ {resultado['iof']:.2f}")
  print(f"Valor líquido após IOF: R$ {resultado['liquido']:.2f}")
  print(f"Cotação do cliente (com spread): R$ {resultado['cotacao_cliente']:.4f}")
  print(f"VET (Valor Efetivo Total): R$ {resultado['vet']:.4f} por {moeda}")
  print(f"Valor que chega em {moeda}: {resultado['convertido']:.2f} {moeda}")

  mostrar_comparativo_investimento(valor_reais, moeda, cotacao_comercial)


if __name__ == "__main__":
  main()