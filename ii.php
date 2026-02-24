<?php
session_start();

// === PASSWORD PROTEKSI ===
$username = "admin";
$password = "password123";

if (!isset($_SESSION['logged_in'])) {
    if (isset($_POST['username']) && isset($_POST['password'])) {
        if ($_POST['username'] === $username && $_POST['password'] === $password) {
            $_SESSION['logged_in'] = true;
        } else {
            echo "Login failed!";
        }
    }

    if (!isset($_SESSION['logged_in'])) {
        echo "<form method='POST'>
                <h2>Login</h2>
                Username: <input type='text' name='username'><br>
                Password: <input type='password' name='password'><br>
                <button type='submit'>Login</button>
              </form>";
        exit;
    }
}

// === FUNGSI FILE MANAGER ===
function listFiles($dir) {
    $files = scandir($dir);
    echo "<h2>PHP File Manager</h2>";
    echo "<p>Current Directory: " . htmlspecialchars($dir) . "</p>";
    echo "<table border='1' cellpadding='5'>";
    echo "<tr><th>Name</th><th>Size</th><th>Permissions</th><th>Actions</th></tr>";

    foreach ($files as $file) {
        $path = $dir . DIRECTORY_SEPARATOR . $file;
        echo "<tr>";
        if (is_dir($path)) {
            echo "<td><a href='?dir=" . urlencode($path) . "'>" . htmlspecialchars($file) . "</a></td>";
            echo "<td>Directory</td><td>-</td><td></td>";
        } else {
            $permissions = substr(sprintf('%o', fileperms($path)), -4);
            echo "<td>" . htmlspecialchars($file) . "</td>";
            echo "<td>" . filesize($path) . " bytes</td>";
            echo "<td>" . $permissions . "</td>";
            echo "<td>
                    <a href='?dir=" . urlencode($dir) . "&download=" . urlencode($file) . "'>Download</a> |
                    <a href='?dir=" . urlencode($dir) . "&delete=" . urlencode($file) . "' onclick='return confirm(\"Are you sure?\")'>Delete</a> |
                    <a href='?dir=" . urlencode($dir) . "&view=" . urlencode($file) . "'>View</a> |
                    <a href='?dir=" . urlencode($dir) . "&edit=" . urlencode($file) . "'>Edit</a> |
                    <a href='?dir=" . urlencode($dir) . "&chmod=" . urlencode($file) . "'>Chmod</a>
                  </td>";
        }
        echo "</tr>";
    }

    echo "</table><br>";

    echo "<form method='POST' enctype='multipart/form-data'>
            <input type='file' name='file'>
            <input type='hidden' name='dir' value='" . htmlspecialchars($dir) . "'>
            <button type='submit' name='upload'>Upload</button>
          </form>";

    echo "<form method='POST'>
            <input type='text' name='new_dir' placeholder='New Folder Name'>
            <input type='hidden' name='dir' value='" . htmlspecialchars($dir) . "'>
            <button type='submit' name='create_dir'>Create Directory</button>
          </form>";

    echo "<br><a href='?dir=" . urlencode(dirname($dir)) . "'>Back to Parent Directory</a>";
}

// === OPERASI FILE MANAGER ===
// Upload file
if (isset($_POST['upload'])) {
    $dir = $_POST['dir'];

    if (!is_writable($dir)) {
        echo "❌ Directory is not writable: $dir<br>";
    }

    if (isset($_FILES['file'])) {
        $targetFile = $dir . DIRECTORY_SEPARATOR . basename($_FILES['file']['name']);
        echo "Upload error: " . $_FILES['file']['error'] . "<br>";

        if (is_uploaded_file($_FILES['file']['tmp_name'])) {
            if (move_uploaded_file($_FILES['file']['tmp_name'], $targetFile)) {
                echo "✅ File uploaded successfully!";
            } else {
                echo "❌ move_uploaded_file() failed.<br>";
            }
        } else {
            echo "❌ is_uploaded_file() failed.<br>";
            echo "Trying fallback method...<br>";
            if (file_put_contents($targetFile, file_get_contents($_FILES['file']['tmp_name']))) {
                echo "✅ Fallback write succeeded!";
            } else {
                echo "❌ Fallback write failed.";
            }
        }
    }
}

// Membuat direktori
if (isset($_POST['create_dir'])) {
    $dir = $_POST['dir'];
    $newDir = $dir . DIRECTORY_SEPARATOR . $_POST['new_dir'];
    if (mkdir($newDir)) {
        echo "✅ Directory created successfully!";
    } else {
        echo "❌ Failed to create directory.";
    }
}

// Menghapus file
if (isset($_GET['delete'])) {
    $fileToDelete = $_GET['dir'] . DIRECTORY_SEPARATOR . $_GET['delete'];
    if (unlink($fileToDelete)) {
        echo "✅ File deleted successfully!";
    } else {
        echo "❌ Failed to delete file.";
    }
}

// Mendownload file
if (isset($_GET['download'])) {
    $fileToDownload = $_GET['dir'] . DIRECTORY_SEPARATOR . $_GET['download'];
    if (file_exists($fileToDownload)) {
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . basename($fileToDownload) . '"');
        header('Content-Length: ' . filesize($fileToDownload));
        readfile($fileToDownload);
        exit;
    } else {
        echo "❌ File not found.";
    }
}

// Melihat isi file
if (isset($_GET['view'])) {
    $fileToView = $_GET['dir'] . DIRECTORY_SEPARATOR . $_GET['view'];
    if (file_exists($fileToView)) {
        echo "<h3>Viewing File: " . htmlspecialchars($_GET['view']) . "</h3>";
        echo "<pre>" . htmlspecialchars(file_get_contents($fileToView)) . "</pre>";
        echo "<a href='?dir=" . urlencode($_GET['dir']) . "'>Back</a>";
        exit;
    } else {
        echo "❌ File not found.";
    }
}

// Mengedit file
if (isset($_GET['edit'])) {
    $fileToEdit = $_GET['dir'] . DIRECTORY_SEPARATOR . $_GET['edit'];
    if (file_exists($fileToEdit)) {
        if (isset($_POST['save'])) {
            file_put_contents($fileToEdit, $_POST['content']);
            echo "✅ File saved successfully!";
        }
        echo "<h3>Editing File: " . htmlspecialchars($_GET['edit']) . "</h3>";
        echo "<form method='POST'>";
        echo "<textarea name='content' rows='20' cols='100'>" . htmlspecialchars(file_get_contents($fileToEdit)) . "</textarea><br>";
        echo "<button type='submit' name='save'>Save</button>";
        echo "</form>";
        echo "<a href='?dir=" . urlencode($_GET['dir']) . "'>Back</a>";
        exit;
    } else {
        echo "❌ File not found.";
    }
}

// Mengubah permission file
if (isset($_GET['chmod'])) {
    $fileToChmod = $_GET['dir'] . DIRECTORY_SEPARATOR . $_GET['chmod'];
    if (file_exists($fileToChmod)) {
        if (isset($_POST['set_permissions'])) {
            $permissions = $_POST['permissions'];
            if (chmod($fileToChmod, octdec($permissions))) {
                echo "✅ Permissions updated successfully!";
            } else {
                echo "❌ Failed to update permissions.";
            }
        }
        echo "<h3>Changing Permissions for: " . htmlspecialchars($_GET['chmod']) . "</h3>";
        echo "<form method='POST'>";
        echo "<label>Set Permissions (e.g., 0755): </label>";
        echo "<input type='text' name='permissions' value='" . substr(sprintf('%o', fileperms($fileToChmod)), -4) . "'><br>";
        echo "<button type='submit' name='set_permissions'>Set Permissions</button>";
        echo "</form>";
        echo "<a href='?dir=" . urlencode($_GET['dir']) . "'>Back</a>";
        exit;
    } else {
        echo "❌ File not found.";
    }
}

// Tampilkan file manager
$dir = isset($_GET['dir']) ? $_GET['dir'] : getcwd();
listFiles($dir);
?>
