import logging       
import logging.handlers   # To create own handler
import smtplib            # Package to send emails


class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, capacity, fromaddr, toaddr, password, subject='Critcal logs'):    # Init method to take email addrs, password, capacity and subject
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.mailhost = 'smtp.gmail.com'
        self.mailport = 465
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.password = password
        self.subject = subject

        self.setFormatter(logging.Formatter(
            '{levelname} - {asctime} - {lineno} - {name} -  In {funcName}: {message}', style='{'))  # Formatter to prettify logs

    def flush(self):        # Method to send emails
        if len(self.buffer) >= self.capacity:        # To avoid sending emails one by one, emails are going to be sent with given capacity
            with smtplib.SMTP_SSL(self.mailhost, self.mailport) as smtp:
                smtp.login(self.fromaddr, self.password) 

                subject = self.subject
                body = f'Review the following critical logs:\n\n'

                for record in self.buffer:
                    body += self.format(record) + '\n'     # Populating body of the message with formatted logs

                msg = f'Subject: {subject}\n\n{body}'

                smtp.sendmail(self.fromaddr, self.toaddr, msg)
                self.buffer.clear()     # Clearing buffer to allude sending same logs

# Example here

logger = logging.getLogger(__name__)    # Creating an instance of logger
handler = BufferingSMTPHandler(5, 'fromaddr', 'toaddr', 'password to fromaddr', 'subject if you wish to change')
handler.setLevel(logging.CRITICAL)     # Set minimum level to receive messages
logger.addHandler(handler)

logger.info('This is info log, which will not be sent')

logger.critical('Critical log! Fix the problem urgently! 1')
logger.critical('Critical log! Fix the problem urgently! 2')
logger.critical('Critical log! Fix the problem urgently! 3')
logger.critical('Critical log! Fix the problem urgently! 4')
logger.critical('Critical log! Fix the problem urgently! 5')

logger.critical('Critical log! Fix the problem urgently! 6')
logger.critical('Critical log! Fix the problem urgently! 7')
logger.critical('Critical log! Fix the problem urgently! 8')
logger.critical('Critical log! Fix the problem urgently! 9')
logger.critical('Critical log! Fix the problem urgently! 10')

# 2 emails has to be sent, first with 1-5 logs and second only with 6-10 logs
