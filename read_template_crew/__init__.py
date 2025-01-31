try:
    from read_template_crew.read_template_crew import EstruturadorCrew, IdentificadorSecoesCrew, LeitorTemplateCrew
except ImportError:
    from .read_template_crew import EstruturadorCrew, IdentificadorSecoesCrew, LeitorTemplateCrew

__all__ = ['EstruturadorCrew', 'IdentificadorSecoesCrew', 'LeitorTemplateCrew']