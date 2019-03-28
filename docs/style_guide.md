|Data|Versão|Alteração|Autor|
|:------:|:------:|:-----:|:-----:|
|28/03/2018|0.1|Criação do documento|Davi Alves|
|28/03/2018|0.2|Adicionar regras PEP para classes e métodos|Davi Alves|

## Python Style

O guia de estilo usado é do Python [PEP 8](https://www.python.org/dev/peps/pep-0008/)

* Use **snake_case**, NÃO camelCase

* O Python 3 não permite misturar o uso de **tabs** e **espaços** para indentação.

* Layout de código
* Use 4 espaços por nível de identação.

Use:
```Python
# Alinhado com o delimitador de abertura.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Adicione 4 espaços (um nível extra de identação) para distinguir os argumentos do restante.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)
```

**NÃO** use:
```Python
# Argumentos proibidos na primeira linha quando não estiver usando alinhamento vertical.
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# Identação adicional exigido como identação não é distinguível.
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```


Use:
```Python
class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
```

**NÃO** use:
```Python
class Person(models.Model):
    FirstName = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=40)
```

* 4 espaço de identação para funções com parâmetros grandes

Use:
```Python
raise AttributeError(
    'Here is a multine error message '
    'shortened for clarity.'
)
```

**NÃO** use:
```Python
raise AttributeError('Here is a multine error message '
                     'shortened for clarity.')
```

* Citação simples para strings

* As funções de docstrings seguem o [PEP 257](https://www.python.org/dev/peps/pep-0257/)

```Python
def test_foo():
    """
    A test docstring looks like this (#123456).
    """
    ...
```

* A classe **Meta** deve ser implementada logo após os atributos da classe e deve ser separada com apenas UMA linha.


```Python
class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'people'
```

