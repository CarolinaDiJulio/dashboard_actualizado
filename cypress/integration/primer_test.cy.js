describe('Mi primera prueba con Cypress', () => {
    it('visita la página de inicio', () => {
      cy.visit('http://localhost:8069/ingresar_views')  // Cambia esta URL por la de tu proyecto
      cy.contains('Bienvenido')  // Asegúrate de que el texto 'Bienvenido' está en la página
    })
  })
  