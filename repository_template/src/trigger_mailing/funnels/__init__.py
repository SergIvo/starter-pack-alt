from .single_mailing import (  # noqa F401
    LeadNavigatedToMainMenu,
    LeadLaunchedSecondMailing,
    MailingWasSentToLead,
    MailingTargetActionAcceptedByLead,
    LeadUnsubscribed,
    router as single_mailing_router,
    FIRST_MAILING_FUNNEL_SLUG,
    SECOND_MAILING_FUNNEL_SLUG,
    task_queue as mailing_task_queue,
)
