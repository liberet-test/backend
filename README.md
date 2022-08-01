# Backend
## Objetivos
Crear un API que se conecte a la base de datos de la aplicación, realizando las siguientes funciones:

### Supplier
---
#### Wallet
- **Hacer una recarga de créditos** a la wallet del usuario
    ~~~sh
    PATCH /supplier/{supplier_id}/wallet/recharge
    ~~~

- **Obtener los eventos** de uso de credito
    ~~~sh
    # Obtener todas las transacciones
    GET /supplier/{supplier_id}/wallet/transaction

    # Obtener las transacciones por id
    GET /supplier/{supplier_id}/wallet/transaction/{transaction_id}
    ~~~
- **Usar servicios** (se podrá usar una vez o N veces - dependiendo del servicio)
    ~~~sh
    # Usar servicio (1 por defecto)
    POST /supplier/{supplier_id}/wallet/service/{service_id}

    # Usar servicio (N veces)
    POST /supplier/{supplier_id}/wallet/service/{service_id}/{quantity}
    ~~~

#### Analitycs
- **Obtener los créditos usados** todos o por servicio <span style="color:orange">(opcional)</span>
    ~~~sh
    # Obtener los créditos usados (todos)
    GET /supplier/{supplier_id}/analitycs/credits

    # Obtener los créditos usados (por servicio)
    GET /supplier/{supplier_id}/analitycs/credits/{service_id}
    ~~~

- **Obtener los dos servicios más usados** <span style="color:orange">(opcional)</span>
    ~~~sh
    # Obtener los dos servicios más usados (2 por defecto)
    GET /supplier/{supplier_id}/analitycs/commonly-used-services

    # Obtener los dos servicios más usados (cantidad requerida)
    GET /supplier/{supplier_id}/analitycs/commonly-used-services/{quantity}
    ~~~

### Service
---
- **Crear nuevos servicios** <span style="color:orange">(Se requieren permisos de administrador) (opcional)</span>
    ~~~sh
    # Crear nuevo servicio
    POST /service/create
    ~~~
- **Obtener la lista de servicios** (uno especifico o todos)
    ~~~sh
    # Obtener todos los servicios
    GET /service

    # Obtener servicio por id
    GET /service/{service_id}
    ~~~
<br>

## Referencias
[Planeación](https://miro.com/app/board/uXjVO_NmmaE=/?share_link_id=466171238038) - Miro board

[Diagrama entidad relación](SS-20220731171812.png)