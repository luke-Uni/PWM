# Password Manager

## **Overview**

This project is a command-line based password manager that allows users to securely store and manage passwords, while also offering additional functionality such as password generation and expiration checks. The tool utilizes encryption (Fernet symmetric encryption) to ensure that passwords are stored securely, and user authentication is enforced through a master password.

## **Features**

- **Master Password Protection**: Secure the password manager with a master password, which is required for all further operations.
- **Password Storage**: Securely store usernames and passwords using symmetric encryption.
- **Password Generation**: Generate strong, random passwords that meet custom requirements.
- **Password Expiration Check**: Identify passwords that are older than 30 days.
- **Password Visibility**: Mask passwords when displayed in the terminal.
- **Clipboard Management**: Copy passwords to the clipboard temporarily (for 30 seconds).
- **Password Modification**: Modify or delete stored passwords.
- **Encryption**: Use SHA-256 and Fernet encryption to protect stored passwords.
- **Master Password Change**: Allows the master password to be updated, with automatic re-encryption of stored data.

## **Setup**

### **Requirements**

- Python 3.x
- Required Python packages:
  - `cryptography`
  - `colorama`

To install the necessary packages, run:

```bash
pip install cryptography colorama
```

Clone this repository:

```bash
git clone <repository-url>
```
Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python password_manager.py
```

## **How to Use**

1. **Initial Setup**: On the first run, the script will prompt you to create a master password. This password is used to encrypt and decrypt your stored data.

2. **Commands**:
   - **`generate`**: Generate a random password based on your specified criteria.
   - **`store`**: Store a username and password associated with a title.
   - **`list`**: List all stored usernames and masked passwords.
   - **`search`**: Search for a password by title.
   - **`delete`**: Delete a stored password by title.
   - **`modify`**: Modify the username or password of a stored entry.
   - **`change`**: Change the master password.
   - **`check`**: Check for passwords that are older than 30 days.
   - **`exit`**: Exit the program.

3. **Password Expiry**: After 30 days, passwords will be flagged as expired and the user will be prompted to update them.

4. **Clipboard Management**: Passwords copied to the clipboard will automatically be cleared after 30 seconds for security.

### **File Structure**

- **`nutzer_info.txt`**: Stores the encrypted user data.
- **`master_info.txt`**: Stores encrypted master password information for validation.

### **Security Features**

- **Master Password Encryption**: Master passwords are hashed using SHA-256 and stored securely.
- **Password Encryption**: All passwords are encrypted with a dynamically created `Fernet` key based on the master password.
- **Password Strength Validation**: The password generator allows users to specify required character types (numbers, uppercase, lowercase, special characters) and generates a secure password accordingly.
- **Time-based Password Expiry**: Alerts when a password is over 30 days old.
