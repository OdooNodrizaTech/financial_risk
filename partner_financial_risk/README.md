El módulo contiene el desarrollo que permite añadir el apartado de Riesgo financiero que sirve para las Ventas

Se implementa la validación de si hay riesgo suficiente justo antes de confirmar la venta
En los modos de pago se añade el campo use_to_calculate_max_credit_limit_allow.
Para calcular el "riesgo vivo" del cliente, se usarán todas facturas o pedidos que tengan los modos de pago con use_to_calculate_max_credit_limit_allow=True
