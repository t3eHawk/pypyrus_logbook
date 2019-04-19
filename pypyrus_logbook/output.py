import os
import smtplib
import datetime as dt
import sqlalchemy as sql

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .utils import py_dir
from .record import Record

def you_shall_not_pass(func):
    def wrapper(output, *args, **kwargs):
        if output.status is True:
            func(output, *args, **kwargs)
    return wrapper

class Output():
    """Class represents any output."""
    def __init__(self, status=False):
        self._status = status
        pass

    def open(self):
        self._status = True
        pass

    def close(self):
        self._status = False
        pass

    @property
    def status(self):
        return self._status

class Branch(Output):
    """Class represents output branches going from the output root."""
    def __init__(self, root, status=False):
        super().__init__(status=status)
        self._root = root
        pass

    @property
    def root(self):
        return self._root

class Root(Output):
    """Class represents output root."""
    def __init__(
        self, logger, console=True, file=True, email=False, html=False,
        table=False, status=True, directory=None, filename=None,
        extension=None, smtp=None, db=None
    ):
        super().__init__(status=status)
        self.logger = logger

        self.console = Console(self, status=console)

        path = dict(dir=directory, name=filename, ext=extension)
        self.file = File(self, status=file, **path)

        smtp = smtp if isinstance(smtp, dict) is True else {}
        self.email = Email(self, status=email, **smtp)

        self.html = HTML(self, status=html)

        db = db if isinstance(db, dict) is True else {}
        self.table = Table(self, status=table, **db)
        pass

    @you_shall_not_pass
    def write(self, record):
        self.console.write(record)
        self.file.write(record)
        self.html.write(record)
        pass

class Console(Branch):
    @you_shall_not_pass
    def write(self, record):
        if isinstance(record, Record) is True:
            record = record.create()
        print(record, end='')
        pass

class File(Branch):
    def __init__(self, root, status=True, dir=None, name=None, ext=None):
        super().__init__(root, status=status)

        dir = dir or os.path.join(py_dir, 'logs')
        name = name or '{app}_{now:%Y%m%d%H%M%S}'
        ext = ext or 'log'
        self.configure(dir=dir, name=name, ext=ext)
        pass

    def configure(self, dir=None, name=None, ext=None):
        if isinstance(dir, str) is True: self.dir = dir
        if isinstance(name, str) is True: self.name = name
        if isinstance(ext, str) is True: self.ext = ext
        if dir is not None or name is not None or ext is not None:
            self.new()
        pass

    @you_shall_not_pass
    def new(self):
        app = self.root.logger.app
        now = dt.datetime.now()
        name = self.name.format(app=app, now=now)

        # Define new path.
        self._path = os.path.abspath(f'{self.dir}/{name}.{self.ext}')

        # Handler and file attributes must be purged.
        self.__handler = None
        self._modified = None
        self._size = None
        pass

    @you_shall_not_pass
    def write(self, record):
        if isinstance(record, Record) is True:
            record = record.create()

        if self.__handler is None:
            # Check the directories.
            dirname = os.path.dirname(self._path)
            if os.path.exists(dirname) is False:
                os.makedirs(dirname)
            # Make file.
            self.__handler = open(self._path, 'a')

        self.__handler.write(record)
        self.__handler.flush()

        self._modified = dt.datetime.now()
        self._size = os.stat(self._path).st_size
        pass

    @property
    def path(self):
        """Absolute path to the file."""
        return self._path

    @property
    def modified(self):
        """Last time when file was modified."""
        return self._modified

    @property
    def size(self):
        """Current file size."""
        return self._size

class Email(Branch):
    """That class represents SMTP server and email used to send notifications
    and alarms generated in the logger.
    """
    def __init__(
        self, root, status=False, address=None, host=None, port=None,
        tls=None, user=None, password=None, recipients=None
    ):
        super().__init__(root, status=status)
        self.configure(
            address=address, host=host, port=port, tls=tls, user=user,
            password=password, recipients=recipients)
        pass

    def configure(
        self, address=None, host=None, port=None, tls=None,
        user=None, password=None, recipients=None
    ):
        if isinstance(host, str) is True:
            self.host = host
        if isinstance(port, int) is True:
            self.port = port
        if isinstance(tls, bool) is True:
            self.tls = tls

        if isinstance(user, str) is True:
            self.user = user
        if isinstance(address, str) is True:
            self.address = address
        if recipients is not None:
            self.recipients = recipients

        if host is not None or port is not None \
        or user is not None or password is not None:
            self.connect(password)
        pass

    @you_shall_not_pass
    def connect(self, password):
        """Method to connect to the SMTP server using the credentials stored
        in the object attributes.
        """
        # Test attributes before connect.
        if hasattr(self, 'host') is False \
        or isinstance(self.host, str) is False:
            raise AttributeError('incorrect host')

        if hasattr(self, 'port') is False \
        or isinstance(self.port, int) is False:
            raise AttributeError('incorrect port')

        self._server = smtplib.SMTP(self.host, self.port)
        if self.tls is True:
            self._server.starttls()

        if self.user is not None:
            if password is None:
                raise AttributeError('can not login without a password')

            self._server.login(self.user, password)
        pass

    @you_shall_not_pass
    def disconnect(self):
        """Method to disconnect from SMTP server."""
        if hasattr(self, '_server') is True:
            self._server.quit()
        pass

    @you_shall_not_pass
    def send(
        self, subject, text, recipients=None, attachment=None, type='html'
    ):
        """Send regular message to the listed addresses."""
        sender = self.address
        recipients = recipients or self.recipients
        if recipients is not None:
            if isinstance(recipients, list) is True:
                recipients = ', '.join(recipients)

            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = recipients
            message['Subject'] = subject

            if text is not None:
                if isinstance(text, list) is False:
                    text = [text]
                for item in text:
                    if isinstance(item, MIMEText) is True:
                        part = item
                        message.attach(part)
                    elif isinstance(item, str) is True:
                        part = MIMEText(item, _subtype=type)
                        message.attach(part)

            if attachment is not None:
                if isinstance(attachment, list) is False:
                    attachment = [attachment]
                for item in attachment:
                    filename = os.path.basename(item)
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(open(item, "rb").read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}")
                    message.attach(part)

            self._server.send_message(message)
        pass

    @you_shall_not_pass
    def alarm(self):
        """Send alarm message to the listed addresses."""
        subject = f'ALARM in {self.root.logger.app}!'

        text = self.root.logger.header.create()
        text = f'<pre>{text}</pre>'
        text = MIMEText(text, 'html')

        attachment = None
        if self.root.file.status is True:
            attachment = self.root.file.path

        recipients = self.recipients
        self.send(subject, text, recipients=recipients, attachment=attachment)
        pass

    @you_shall_not_pass
    def write(self, record):
        pass

class HTML(Branch):
    def __init__(self, root, status=False, dir=None, filename=None):
        super().__init__(root, status=status)
        pass

    def configure(self, dir=None, filename=None):
        pass

    @you_shall_not_pass
    def write(self, record):
        pass

class Table(Branch):
    def __init__(
        self, root, status=False, vendor=None, host=None, port=None, sid=None,
        user=None, password=None, schema=None, table=None, entity=None,
        db=None
    ):
        super().__init__(root, status=status)
        self.configure(
            vendor=vendor, host=host, port=port, sid=sid, user=user,
            password=password, schema=schema, table=table,
            entity=entity, db=db)
        pass

    def configure(
        self, vendor=None, host=None, port=None, sid=None, user=None,
        password=None, schema=None, table=None, entity=None, db=None
    ):
        if isinstance(vendor, str) is True:
            self.vendor = vendor.lower()
        if isinstance(host, str) is True:
            self.host = host.lower()
        if isinstance(port, int) is True:
            self.port = port
        if isinstance(sid, str) is True:
            self.sid = sid.lower()
        if isinstance(user, str) is True:
            self.user = user.lower()
        if isinstance(schema, str) is True:
            self.schema = schema.lower()
        if isinstance(table, str) is True:
            self.table = table.lower()

        if isinstance(db, sql.engine.base.Connection) is True:
            self._db = db
        elif isinstance(db, sql.engine.base.Engine) is True:
            self._db = db.connect()
        elif host is not None or port is not None or sid is not None \
        or user is not None or password is not None:
            self.connect(password)

        if isinstance(entity, sql.sql.schema.Table) is True:
            self._entity = entity
            self._id = None
        elif table is not None:
            self.new()
        pass

    @you_shall_not_pass
    def connect(self, password):
        # Test attributes before connect.
        if hasattr(self, 'vendor') is False \
        or isinstance(self.vendor, str) is False:
            raise AttributeError('incorrect vendor name')

        if hasattr(self, 'sid') is False \
        or isinstance(self.sid, str) is False:
            raise AttributeError('incorrect SID')

        if self.vendor == 'sqlite':
            credentials = f'{self.vendor}:///{self.sid}'
        else:
            if hasattr(self, 'host') is False \
            or isinstance(self.host, str) is False:
                raise AttributeError('incorrect host')

            if hasattr(self, 'port') is False \
            or isinstance(self.port, int) is False:
                raise AttributeError('incorrect port')

            if hasattr(self, 'user') is False \
            or isinstance(self.user, str) is False:
                raise AttributeError('can not login without a username')

            if isinstance(password, str) is False:
                raise AttributeError('can not loging without a password')

            login = f'{self.user}:{password}'
            address = f'{self.host}:{self.port}/{self.sid}'
            credentials = f'{self.vendor}://{login}@{address}'

        engine = sql.create_engine(credentials)
        self._db = engine.connect()
        pass

    @you_shall_not_pass
    def new(self):
        # Get table.
        self._metadata = sql.MetaData()
        self._entity = sql.Table(
            self.table, self._metadata,
            autoload=True, autoload_with=self._db,
            schema=self.schema)
        self._id = None
        pass

    @you_shall_not_pass
    def disconnect(self):
        if hasattr(self, '_db') is True:
            self._db.close()
        pass

    @you_shall_not_pass
    def write(self, **values):
        primary_key = self._entity.primary_key.columns
        if self._id is None:
            insert = self._entity.insert().values(**values)
            insert = insert.returning(*primary_key)
            self._id = self._db.execute(insert).scalar()
        else:
            update = self._entity.update().values(**values)
            for column in primary_key:
                update = update.where(column==self._id)
            self._db.execute(update)
        pass

    @property
    def pointer(self):
        return self._id
