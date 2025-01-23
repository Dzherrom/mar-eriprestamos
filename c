{% extends "layouts/base.html" %}
{% load static %}
{% block content %}

<div class="container">
    <div class="card">        
        <div class="card-header">
            <h4 class="card-title">Editar Pago</h4>
        </div>
    {% if errors %}
    <div class="alert alert-danger">
        <strong>Errores:</strong>
        <ul>
            {% for field, error_list in errors.items %}
                <li>{{ field }}: {{ error_list|join:", " }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
    <div class="card-body">
        <div class="cliente-form-container">
            <form method="post" action="{% url 'pago_editar' pago.id %}">
                {% csrf_token %}
                <!-- Campo: Cliente -->
                <div class="form-group">
                    <div>
                        <label for="id_cliente">Cliente:</label>
                        <select name="cliente" id="id_cliente" class="form-control" required>
                            {% for cliente in clientes %}
                                <option value="{{ cliente.id }}">{{ cliente.nombre }} {{ cliente.apellido }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>

                <!-- Campo: Fecha de Pago -->
                <div class="form-group">
                    <div>
                        <label for="id_fecha_pago">Fecha de Pago:</label>
                        <input type="date" name="fecha_pago" id="id_fecha_pago" class="form-control" required>
                    </div>
                </div>

                <!-- Campo: Moneda -->
                <div class="form-group">
                    <div>
                        <label for="id_moneda">Moneda:</label>
                        <select name="moneda" id="id_moneda" class="form-control" required>
                            {% for moneda in monedas %}
                                <option value="{{ moneda.id }}">{{ moneda }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>

                <!-- Campo: Tipo de Pago -->
                <div class="form-group">
                    <div>
                        <label for="id_tipo_pago">Tipo de Pago:</label>
                        <select name="tipo_pago" id="id_tipo_pago" class="form-control" required>
                            {% for tipo_pago in tipos_pago %}
                                <option value="{{ tipo_pago.id }}">{{ tipo_pago }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>

                <!-- Campo: Referencia -->
                <div class="form-group">
                    <div>
                        <label for="id_referencia">Referencia:</label>
                        <input type="text" name="referencia" id="id_referencia" class="form-control" required>
                    </div>
                </div>

                <!-- Campo: Monto -->
                <div class="form-group">
                    <div>
                        <label for="id_monto">Monto:</label>
                        <input type="number" name="monto" id="id_monto" class="form-control" required>
                    </div>
                </div>

                <!-- Campo: Préstamo -->
                <div class="form-group">
                    <div>
                        <label for="id_prestamo">Préstamo:</label>
                        <select name="prestamo" id="id_prestamo" class="form-control">
                            {% for prestamo in prestamos %}
                                <option value="{{ prestamo.id }}">{{ prestamo }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>

                <!-- Botones de Acción -->
                <div class="button-group">
                    <div class="form-group text-center">
                        <!-- Botón de Guardar -->
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save"></i> Guardar
                        </button>

                        <!-- Botón de Limpiar Campos -->
                        <button type="reset" class="btn btn-secondary">
                            <i class="fas fa-eraser"></i> Limpiar Campos
                        </button>

                        <!-- Boton de Volver -->
                        <a type="cancel" href="{% url 'pagos' %}" class="btn btn-danger">
                            Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
</div>

{% endblock content %}
