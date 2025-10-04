# Building for All Platforms Using GitHub Actions (FREE)

This guide shows you how to use GitHub Actions to automatically build executables for Windows, macOS, and Linux **without needing access to those platforms**.

## 🎯 What This Does

- ✅ Builds for Windows, macOS, and Linux automatically
- ✅ 100% FREE (GitHub Actions is free for public repos)
- ✅ No need to own a Mac or Windows PC
- ✅ Creates downloadable packages with instructions
- ✅ Can create releases automatically

## 📋 Prerequisites

1. A GitHub account (free)
2. Your project code uploaded to GitHub

## 🚀 Setup Instructions

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name it: `polygon-mapper`
4. Make it **Public** (for free Actions) or Private (limited free minutes)
5. Click "Create repository"

### Step 2: Upload Your Code

```bash
# In your polygon-mapper folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/polygon-mapper.git
git push -u origin main
```

### Step 3: Add GitHub Actions Workflow

1. In your local `polygon-mapper` folder, create:
   ```bash
   mkdir -p .github/workflows
   ```

2. Create the file `.github/workflows/build.yml` with the content from the artifact I just created

3. Commit and push:
   ```bash
   git add .github/workflows/build.yml
   git commit -m "Add GitHub Actions workflow"
   git push
   ```

### Step 4: Trigger a Build

**Option A: Create a Release Tag**
```bash
git tag v1.0
git push origin v1.0
```

**Option B: Manual Trigger**
1. Go to your GitHub repo
2. Click "Actions" tab
3. Click "Build Executables" workflow
4. Click "Run workflow"
5. Click the green "Run workflow" button

### Step 5: Download Your Executables

1. Go to "Actions" tab on GitHub
2. Click on the completed workflow run
3. Scroll to "Artifacts" section
4. Download:
   - `PolygonMapper-Windows.zip`
   - `PolygonMapper-macOS.zip`
   - `PolygonMapper-Linux.tar.gz`

That's it! You now have executables for all three platforms! 🎉

## 📦 What You Get

Each artifact contains:
- The executable for that platform
- HOW_TO_USE.txt with simple instructions
- Ready to distribute to users

## 🔄 Creating Official Releases

If you pushed a version tag (like `v1.0`), the workflow automatically creates a GitHub Release with all three executables attached!

To create a new release:
```bash
git tag v1.1
git push origin v1.1
```

Then users can download from: `https://github.com/YOUR_USERNAME/polygon-mapper/releases`

## 💰 Cost

**Free tier includes:**
- 2,000 minutes/month for private repos
- Unlimited for public repos
- Each build takes ~5-10 minutes total (all 3 platforms in parallel)

So even with private repos, you can do 200+ builds per month for free!

## 🛠️ Customization

### Change Python Version
In `build.yml`, modify:
```yaml
python-version: '3.11'  # Change to 3.8, 3.9, 3.10, etc.
```

### Add More Files to Package
In the "Package" steps, add more files:
```yaml
zip -r PolygonMapper-macOS.zip PolygonMapper HOW_TO_USE.txt LICENSE.txt
```

### Build Only on Main Branch Commits
Change the trigger:
```yaml
on:
  push:
    branches:
      - main
```

## 🐛 Troubleshooting

**Build fails with "templates not found":**
- The workflow handles this automatically with the timeout step
- If issues persist, commit an empty `templates` folder

**Actions tab not showing:**
- Make sure you pushed the `.github/workflows/build.yml` file
- Check it's in the correct path

**Out of minutes:**
- Public repos have unlimited minutes
- Or build locally instead

**Can't download artifacts:**
- Artifacts expire after 90 days by default
- Use releases for permanent downloads

## 📝 Alternative: Just the Artifacts (No Release)

If you don't want automatic releases, remove this section from `build.yml`:
```yaml
    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/')
      uses: softprops/action-gh-release@v1
      with:
        files: dist/${{ matrix.asset_name }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Then just download from the "Artifacts" section after each workflow run.

## 🎯 Quick Reference

```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/polygon-mapper.git
git push -u origin main

# Create release
git tag v1.0
git push origin v1.0

# Update and rebuild
git add .
git commit -m "Update features"
git tag v1.1
git push origin v1.1
```

## ✨ Benefits of This Approach

1. **No Virtual Machines needed** - GitHub provides them
2. **Consistent builds** - Same environment every time
3. **Version control** - Every build is tagged and traceable
4. **Easy distribution** - Users download from GitHub releases
5. **Free** - No cost for public repos
6. **Fast** - Builds run in parallel (all 3 platforms at once)

---

**You can now build for Windows, macOS, and Linux from ANY computer, even a Raspberry Pi!** 🚀
