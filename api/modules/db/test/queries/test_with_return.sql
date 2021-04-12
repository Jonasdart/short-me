Select 
    fildoc, 
    doc, 
    serie, 
    datacad, 
    count(*)
from 
    assinatura_cliente
where 
    datacad >= '20201201'
group by 
    fildoc, 
    doc, 
    serie, 
    datacad
having 
    count(*) > 1